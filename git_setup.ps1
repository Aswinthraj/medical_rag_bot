# Git setup and commit script
cd d:\Development\medical_rag_bot

# Remove lock file if it exists
if (Test-Path .git\index.lock) {
    Remove-Item .git\index.lock -Force
}

# Configure git
git config user.name "Aswinthraj"
git config user.email "femilinaswinthraj731@gmail.com"

# Stage all files
git add .

# Create commit with co-author
$commitMsg = @"
Initial commit: Medical RAG Bot project

Co-authored-by: hari632 <harinidars@gmail.com>
"@

git commit -m $commitMsg

# Show status
git log -1 --pretty=full
