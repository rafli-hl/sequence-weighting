<#
Reusable owner command for N8's Runs R3-R8 (N8-protocol-draft.md, sections 8 and 10). Each run takes two calls, in this order:

  & 'D:\sequence-weighting-n8\RUN_COMMAND.ps1' -Run <k> -Step Build -ApprovalId OWNER-<yyyymmdd>-N8-R<k>-<nn> -ApprovalText '<your approval text>'
  & 'D:\sequence-weighting-n8\RUN_COMMAND.ps1' -Run <k> -Step Run

Build makes the run's one-use activation: native Python, no GPU. It reads and checks the corpus, which lies in the closed record's
work/runs/, so only the owner runs it. Run is the run itself: GPU, about 2.3 h wall time (2.1 h on the worker clock, at most 6 h on the
worker clock). Call it only after Build printed "status": "ARMED_UNUSED" and build exit=0; on AC power with the lid open, no games or
other GPU apps; keep the window open. Before the owner script claims the run, the Run step reads the GPU's memory with nvidia-smi and
refuses over 600 MiB, listing the processes on the GPU (OPERATIONAL_NOTES.md, 16 November 2026). That covers the start only: open no
GPU app until the run ends, since in R2 another app's memory stopped the worker in its last draw.
The approval is yours, given for each run: the id must name Run R<k> (OWNER-<yyyymmdd>-N8-R<k>-<nn>, with a real date), and the text
must name Run R<k>, its three draws and the id, and no other run or draw. It is checked before anything is read. Everything else follows
from the run number and is checked as R2_COMMAND.txt checks it; in addition, if Run R<k-1> did not complete, Build waits until its retry
run X<k-1> has ended. R1 and R2 have their own commands; a retry run X<k> needs its own.
#>
param(
  [Parameter(Mandatory=$true)][ValidateRange(3, 8)][int]$Run,
  [Parameter(Mandatory=$true)][ValidateSet('Build', 'Run')][string]$Step,
  [string]$ApprovalId,
  [string]$ApprovalText
)
$ErrorActionPreference = 'Stop'
$study = 'D:\sequence-weighting-n8'
$subject = '9bdea3a9715b05393afe6713ddc696834dd344c3485c4e1a6ed0fa222f44bb6b'
$k = $Run; $prev = $k - 1
$draws = @(1..3 | ForEach-Object { 'n{0:d2}' -f (3 * ($k - 1) + $_) })
$activation = "$study\activations\n8-r$k"

if ($Step -eq 'Run') {
  if ($ApprovalId -or $ApprovalText) { throw 'The Run step takes no approval: the Build step recorded it. Nothing was claimed' }
  # The worker makes its run folder inside runs, and the owner script claims before the worker starts, so runs must exist first.
  if (-not (Test-Path -LiteralPath "$study\runs" -PathType Container)) { throw "Missing folder: $study\runs, which holds the earlier runs. Stop and report it; nothing was claimed" }
  if (-not (Test-Path -LiteralPath "$activation\AUTHORIZATION.json" -PathType Leaf)) { throw "Run R$k is not built: $activation has no AUTHORIZATION.json. Do the Build step first; nothing was claimed" }
  # GPU memory before the claim (an operational precaution of 16 November 2026, OPERATIONAL_NOTES.md; no sealed file changes). Read only:
  # five nvidia-smi readings of the GPU memory used, 1 s apart; if any is over 600 MiB, nothing is claimed. Either way it lists the
  # processes on the GPU, with the dedicated GPU memory Windows counts for each, so you can close them.
  $smi = 'C:\Windows\System32\nvidia-smi.exe'
  if (-not (Test-Path -LiteralPath $smi -PathType Leaf)) { throw "nvidia-smi not found at $smi. Nothing was claimed" }
  $used = @(foreach ($i in 1..5) {
    if ($i -gt 1) { Start-Sleep -Seconds 1 }
    $r = @(& $smi '--query-gpu=memory.used' '--format=csv,noheader,nounits')
    if ($LASTEXITCODE -ne 0 -or $r.Count -ne 1 -or "$($r[0])".Trim() -notmatch '^[0-9]+$') { throw 'nvidia-smi did not report the memory used of one GPU. Nothing was claimed' }
    [int]"$($r[0])".Trim()
  })
  $gpuMib = @{}
  try { foreach ($s in (Get-Counter '\GPU Process Memory(*)\Dedicated Usage' -ErrorAction Stop).CounterSamples) { if ($s.InstanceName -match '^pid_([0-9]+)_') { $gpuMib[[int]$Matches[1]] += $s.CookedValue / 1MB } } } catch {}
  $apps = @(& $smi '--query-compute-apps=pid,process_name' '--format=csv,noheader' | Where-Object { "$_".Trim() } | ForEach-Object {
    $f = "$_".Split(',', 2); $appId = 0; [void][int]::TryParse($f[0].Trim(), [ref]$appId); $name = if ($f.Count -gt 1) { $f[1].Trim() } else { '' }
    if (-not $name -or $name.StartsWith('[')) { try { $name = (Get-Process -Id $appId -ErrorAction Stop).ProcessName } catch {} }
    [pscustomobject]@{ PID = $appId; MiB = $(if ($gpuMib.ContainsKey($appId)) { [math]::Round($gpuMib[$appId]) } else { $null }); Process = $name }
  })
  'GPU memory used before the claim: ' + ($used -join ', ') + ' MiB (limit 600 MiB). Processes on the GPU (nvidia-smi), with the dedicated GPU memory in MiB that Windows counts for each:'
  if ($apps.Count -gt 0) { ($apps | Sort-Object MiB -Descending | Format-Table -AutoSize | Out-String -Width 250).TrimEnd() } else { '  none listed' }
  $top = ($used | Measure-Object -Maximum).Maximum
  if ($top -gt 600) { throw ('The GPU has ' + $top + ' MiB in use, over the 600 MiB limit. Close the apps listed above that you opened (games, browsers, video, GPU tools), then run the same command again. Nothing was claimed') }
  & "$activation\MATCHED_OWNER_RUN.ps1" -ExpectedSubject $subject
  return
}

# The approval, given by the owner for this run and naming it; checked before anything is read.
if (-not $ApprovalId -or -not $ApprovalText) { throw 'The Build step needs -ApprovalId and -ApprovalText. Nothing was built' }
$id = [regex]::Match($ApprovalId, ('^OWNER-([0-9]{{8}})-N8-R{0}-[0-9]{{2}}$' -f $k))
if (-not $id.Success) { throw ('The approval id must name Run R{0}: OWNER-<yyyymmdd>-N8-R{0}-<nn>. Nothing was built' -f $k) }
$day = [datetime]::MinValue
if (-not [datetime]::TryParseExact($id.Groups[1].Value, 'yyyyMMdd', [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::None, [ref]$day)) { throw ('The approval id''s date is not a date: ' + $id.Groups[1].Value + '. Nothing was built') }
$runsNamed = @([regex]::Matches($ApprovalText, '\b[RX][0-9]+\b') | ForEach-Object { $_.Value } | Sort-Object -Unique)
$drawsNamed = @([regex]::Matches($ApprovalText, '\bn[0-9]{2}\b') | ForEach-Object { $_.Value } | Sort-Object -Unique)
if (-not [regex]::IsMatch($ApprovalText, ('\bRun R{0}\b' -f $k)) -or -not $ApprovalText.Contains($ApprovalId) -or ($runsNamed -join ',') -cne "R$k" -or ($drawsNamed -join ',') -cne ($draws -join ',')) {
  throw ('The approval text must name Run R{0}, its draws {1} and the approval id, and no other run or draw. Nothing was built' -f $k, ($draws -join ', '))
}
if ($ApprovalText.Contains('"') -or $ApprovalText.Contains('\')) { throw 'The approval text must not contain double quotes or backslashes (they do not reach the builder intact). Nothing was built' }

# The builder with the registration recorded, the registered source and the pilot's log, against their hashes.
$src = "$study\source"
if ((Get-FileHash -LiteralPath "$study\tools\build_n8_activation.py" -Algorithm SHA256).Hash.ToLower() -ne 'c31fd4aa32873a1d025621f06bcc66e289c16ad86f64612c00dad76b1fd62904') { throw 'Hash differs: tools\build_n8_activation.py' }
if ((Get-FileHash -LiteralPath "$src\SOURCE_SUBJECT.json" -Algorithm SHA256).Hash.ToLower() -ne $subject) { throw 'Hash differs: source\SOURCE_SUBJECT.json' }
foreach ($row in (Get-Content -LiteralPath "$src\SOURCE_SUBJECT.json" -Raw -Encoding UTF8 | ConvertFrom-Json).files) { if ((Get-FileHash -LiteralPath (Join-Path $src $row.path) -Algorithm SHA256).Hash.ToLower() -ne $row.sha256) { throw ('Changed source ' + $row.path) } }
if ((Get-FileHash -LiteralPath "$study\pilot\PILOT_LOG.json" -Algorithm SHA256).Hash.ToLower() -ne '251d0951e30250afa16cb998b06550358c09234d8a24c45166b08d0642347db6') { throw 'Hash differs: pilot\PILOT_LOG.json' }
foreach ($d in "$src\__pycache__", "$src\vendor\__pycache__", "$study\tools\__pycache__") { if (Test-Path -LiteralPath $d) { throw "Bytecode folder exists: $d" } }
'All files match'
# The registration is public: GitHub has the tag n8-registration at the merge commit (protocol section 10, step 5).
$tag = @(git -C 'C:\Users\rafli\sequence-weighting' ls-remote origin 'refs/tags/n8-registration' 'refs/tags/n8-registration^{}')
if (-not ($tag | Where-Object { "$_".StartsWith('c6f98b26669f5d29f30c576b6d800c1fc82c98eb') })) { throw 'GitHub has no tag n8-registration at the merge commit c6f98b26669f5d29f30c576b6d800c1fc82c98eb. Push it first: git -C C:\Users\rafli\sequence-weighting push origin refs/tags/n8-registration' }
'GitHub has the tag n8-registration at the merge commit'
# Once only: the run's activation and run folders do not exist yet.
foreach ($d in $activation, "$study\runs\n8-r$k") { if (Test-Path -LiteralPath $d) { throw "Exists already: $d. R$k is built and run once" } }
# The two parent folders must exist: the builder makes only the activation folder, and the worker only its run folder.
foreach ($d in "$study\activations", "$study\runs") { if (-not (Test-Path -LiteralPath $d -PathType Container)) { throw "Missing folder: $d, which holds the earlier runs' folders. Stop and report it; nothing was built" } }
# Registry order (protocol section 8), one run at a time: the run before this one has ended, so its owner script wrote its exit receipt;
# if it did not complete, its retry run X<k-1> has ended too, so the draws it repeats come before this run's (owner, 16 November 2026).
if (-not (Test-Path -LiteralPath "$study\activations\n8-r$prev\OWNER_EXIT_RECEIPT.json" -PathType Leaf)) { throw "Run R$prev has not ended: activations\n8-r$prev has no OWNER_EXIT_RECEIPT.json. Runs go in registry order (protocol section 8)" }
$before = Get-Content -LiteralPath "$study\activations\n8-r$prev\OWNER_EXIT_RECEIPT.json" -Raw -Encoding UTF8 | ConvertFrom-Json
if ($before.status -ne 'COMPLETE' -and -not (Test-Path -LiteralPath "$study\activations\n8-x$prev\OWNER_EXIT_RECEIPT.json" -PathType Leaf)) { throw "Run R$prev did not complete (status $($before.status)) and its retry run X$prev has not ended: activations\n8-x$prev has no OWNER_EXIT_RECEIPT.json. Run X$prev first; runs go in registry order (protocol section 8)" }
# Room on D:: every run after R1 needs at least 3 GiB free (the worker's admission rule); its owner script checks again before its claim.
$free = (Get-PSDrive D).Free
if ($free -lt 3GB) { throw ('Run R' + $k + ' needs at least 3 GiB free on D:; free now ' + [math]::Round($free / 1GB, 2) + ' GiB') }
'Building the activation of Run R' + $k + ' (' + ($draws -join ', ') + '). It checks every corpus file, which takes a few minutes; keep this window open.'
& 'C:\Users\rafli\AppData\Local\Programs\Python\Python312\python.exe' -I -B "$study\tools\build_n8_activation.py" --mode "R$k" --approval-id $ApprovalId --user-text $ApprovalText
"build exit=$LASTEXITCODE"
if ($LASTEXITCODE -eq 0) { "Next, if the output above shows ""status"": ""ARMED_UNUSED"": & '$study\RUN_COMMAND.ps1' -Run $k -Step Run" }
