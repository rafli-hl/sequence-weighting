# POST HOC audit script (area D). Tests two pieces of the published RUN_COMMAND.ps1 on DUMMY folders inside the auditor's scratch
# folder: (1) the run-order rule (its lines 93-95), (2) the approval checks (its lines 63-73). The lines are taken from the published
# file by line number and executed unchanged, with $study pointed at a dummy folder. RUN_COMMAND.ps1 itself is never run; nothing on
# drive D: is touched; no builder, git, nvidia-smi or owner script is called (those lines are not among the ones extracted).
param([Parameter(Mandatory=$true)][string]$Clone, [Parameter(Mandatory=$true)][string]$Scratch)
$ErrorActionPreference = 'Stop'
$published = Join-Path $Clone 'preregistration\natural-text-dense-replication-20261114\RUN_COMMAND.ps1'
$lines = [IO.File]::ReadAllLines($published)
$orderRule = ($lines[92..94] -join "`n")        # lines 93-95 (1-based)
$approval = ($lines[62..72] -join "`n")         # lines 63-73
foreach ($bad in 'D:\', 'git ', 'nvidia', 'python', 'MATCHED_OWNER_RUN', 'build_n8') { if ($orderRule.Contains($bad) -or $approval.Contains($bad)) { throw "extracted lines contain $bad" } }
'--- the extracted run-order lines (93-95), first 110 characters of each:'
$lines[92..94] | ForEach-Object { '    ' + $_.Substring(0, [Math]::Min(110, $_.Length)) }

$dummy = Join-Path $Scratch 'ps-dummy-study'
if (-not $dummy.Contains('swa21\d\scratch')) { throw 'dummy path is not in the scratch folder' }
function Reset-Dummy { if (Test-Path -LiteralPath $dummy) { Remove-Item -LiteralPath $dummy -Recurse -Force -Confirm:$false }; New-Item -ItemType Directory -Force -Path (Join-Path $dummy 'activations') | Out-Null }
function Put-Receipt([string]$mode, [string]$status) {
  $d = Join-Path $dummy ('activations\n8-' + $mode.ToLower()); New-Item -ItemType Directory -Force -Path $d | Out-Null
  [IO.File]::WriteAllText((Join-Path $d 'OWNER_EXIT_RECEIPT.json'), (@{status=$status; mode=$mode} | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
}
function Test-Order([string]$label, [scriptblock]$setup) {
  Reset-Dummy; & $setup
  $study = $dummy; $k = 3; $prev = 2
  try { Invoke-Expression $orderRule; "  PROCEEDS  $label" } catch { $m = "$($_.Exception.Message)"; "  STOPS     $label   [" + $m.Substring(0, [Math]::Min(95, $m.Length)) + ']' }
}
'--- (1) run order, Build step of R3 (k = 3, the run before it is R2)'
Test-Order 'no exit receipt of R2' { }
Test-Order 'R2 FAILED, no exit receipt of X2' { Put-Receipt 'R2' 'FAILED' }
Test-Order 'R2 FAILED, X2 built but never claimed (activation folder, no exit receipt)' { Put-Receipt 'R2' 'FAILED'; New-Item -ItemType Directory -Force -Path (Join-Path $dummy 'activations\n8-x2') | Out-Null }
Test-Order 'R2 FAILED, X2 ended COMPLETE' { Put-Receipt 'R2' 'FAILED'; Put-Receipt 'X2' 'COMPLETE' }
Test-Order 'R2 FAILED, X2 ended FAILED' { Put-Receipt 'R2' 'FAILED'; Put-Receipt 'X2' 'FAILED' }
Test-Order 'R2 COMPLETE, no X2' { Put-Receipt 'R2' 'COMPLETE' }
Test-Order 'R2 STOPPED_AT_STARTUP, no X2' { Put-Receipt 'R2' 'STOPPED_AT_STARTUP' }
Test-Order 'R2 EXIT_UNOBSERVED_NO_KILL, no X2' { Put-Receipt 'R2' 'EXIT_UNOBSERVED_NO_KILL' }

function Test-Approval([string]$label, [string]$ApprovalId, [string]$ApprovalText) {
  $k = 3; $draws = @(1..3 | ForEach-Object { 'n{0:d2}' -f (3 * ($k - 1) + $_) })
  try { Invoke-Expression $approval; "  ACCEPTED  $label" } catch { $m = "$($_.Exception.Message)"; "  REFUSED   $label   [" + $m.Substring(0, [Math]::Min(80, $m.Length)) + ']' }
}
'--- (2) approval checks, Build step of R3 (draws n07, n08, n09)'
Test-Approval 'id and text name Run R3, n07-n09 and the id' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08, n09) under OWNER-20991231-N8-R3-01.'
Test-Approval 'no approval given' '' ''
Test-Approval 'id names R4' 'OWNER-20991231-N8-R4-01' 'I approve N8 Run R3 (draws n07, n08, n09) under OWNER-20991231-N8-R4-01.'
Test-Approval 'id date is not a date' 'OWNER-20991341-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08, n09) under OWNER-20991341-N8-R3-01.'
Test-Approval 'text names a second run' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 and R4 (draws n07, n08, n09) under OWNER-20991231-N8-R3-01.'
Test-Approval 'text names a wrong draw' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08, n10) under OWNER-20991231-N8-R3-01.'
Test-Approval 'text lacks a draw' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08) under OWNER-20991231-N8-R3-01.'
Test-Approval 'text lacks the id' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08, n09).'
Test-Approval 'text has a double quote' 'OWNER-20991231-N8-R3-01' 'I approve N8 Run R3 (draws n07, n08, n09) "now" under OWNER-20991231-N8-R3-01.'
Reset-Dummy
