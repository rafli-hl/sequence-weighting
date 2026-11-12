# GitHub pull-request snapshots, 11 November 2026

Read-only copies of the GitHub API responses for the pull requests that the record cites, taken on 11 November 2026 at
08:24 UTC. Pull request pages, comments and reviews live on GitHub's side and do not move with the git history. These
copies keep them with the record. Pull request #3 was saved earlier, in
[`pr3-gh-snapshot-20261104`](../natural-text-peak-result-20261103-01/pr3-gh-snapshot-20261104/).

| Pull request | What it did | Merged (UTC) | Merge commit |
|---|---|---|---|
| [#1](pr1/) | Catalogue of the v0135 and v0136 results | 8 Oct 2026, 09:22 | `1e0980b` |
| [#4](pr4/) | Publication of the natural-text studies, the adversarial review and its response | 4 Nov 2026, 06:05 | `332aa76` |
| [#5](pr5/) | **Public registration of N7**, before any of its runs | 5 Nov 2026, 04:44 | `f3a2571`, signed by GitHub |
| [#6](pr6/) | Publication of N7's result | 6 Nov 2026, 06:46 | `4e3baae` |

Each folder holds the responses, as returned and compacted to one line, of these REST calls on
`repos/rafli-hl/sequence-weighting-research`, the repository where the record was built (now private):

| File | Call |
|---|---|
| `pr.json` | `pulls/<n>`: title, description, author, times, merge commit |
| `comments.json` | `issues/<n>/comments`: the conversation |
| `review_comments.json` | `pulls/<n>/comments`: comments on lines of the diff |
| `reviews.json` | `pulls/<n>/reviews` |
| `timeline.json` | `issues/<n>/timeline`: commits, reviews, merge and close events |

**Left out.** The list of each pull request's commits, because the commits are in the git history of the repository where the
record was built, archived at Software Heritage (see "Where this record was built" in the
[README](../../README.md#where-this-record-was-built)); PR #1's timeline,
because its commit events repeat a personal email address that is already in the history; and the edit history of the
descriptions, which GitHub serves only through an API not available when the copies were made. Empty lists (`[]`) mean
the pull request had none.

**What they show and what they don't.** The copies were made by the owner's AI assistant (Claude Opus 5.5) with
read-only `gh api` calls; they are a record of what GitHub reported on that day, not independent evidence. The
independent evidence of N7's registration time is the merge commit `f3a2571`, which GitHub signed when it merged pull
request #5 and which any copy of the history carries.
