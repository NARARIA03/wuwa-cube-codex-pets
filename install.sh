#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
target="${CODEX_HOME:-$HOME/.codex}/pets/aemeath-cube"

if [ -e "$target" ] || [ -L "$target" ]; then
  printf '이미 설치 경로가 있습니다. 기존 파일을 백업한 뒤 다시 실행해 주세요: %s\n' "$target" >&2
  exit 1
fi

for file in pet.json spritesheet.png; do
  if [ ! -f "$repo_dir/pet/$file" ]; then
    printf '설치 파일이 없습니다: %s\n' "$repo_dir/pet/$file" >&2
    exit 1
  fi
done

mkdir -p "$(dirname -- "$target")"
mkdir "$target"
cp "$repo_dir/pet/pet.json" "$repo_dir/pet/spritesheet.png" "$target/"

printf '설치 완료: %s\n' "$target"
printf 'Codex의 Settings → Pets에서 목록을 새로고침하고 에이메스 큐브을 선택하세요.\n'
