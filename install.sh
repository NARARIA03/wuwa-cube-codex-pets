#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
pets_dir="${CODEX_HOME:-$HOME/.codex}/pets"

usage() {
  printf '사용법: ./install.sh [펫 ID | --all | --list]\n인자 없이 실행하면 설치 메뉴를 엽니다.\n'
}

install_pet() {
  source_dir="$repo_dir/pets/$1"
  target="$pets_dir/$1"
  if [ -e "$target" ] || [ -L "$target" ]; then
    printf '건너뜀 (이미 설치됨): %s\n' "$1"
    return
  fi
  mkdir "$target"
  if ! cp "$source_dir/pet.json" "$source_dir/spritesheet.png" "$target/"; then
    rm -f "$target/pet.json" "$target/spritesheet.png"
    rmdir "$target"
    return 1
  fi
  printf '설치 완료: %s\n' "$target"
}

if [ "$#" -gt 1 ]; then
  usage >&2
  exit 1
fi
requested=${1:-}
case "$requested" in -h|--help) usage; exit 0 ;; esac

# Each package lives in pets/<id>/ and contains only its installable assets.
set --
for directory in "$repo_dir"/pets/*; do
  [ -f "$directory/pet.json" ] || continue
  set -- "$@" "${directory##*/}"
done
[ "$#" -gt 0 ] || { printf '설치할 펫이 없습니다.\n' >&2; exit 1; }

if [ "$requested" = --list ]; then
  printf '%s\n' "$@"
  exit 0
fi

if [ -z "$requested" ]; then
  printf 'Wuwa Cube Codex Pets\n\n'
  index=1
  for id do
    printf '  %s) %s\n' "$index" "$id"
    index=$((index + 1))
  done
  printf '  a) 전체 설치\n  0) 취소\n\n선택: '
  IFS= read -r choice || exit 1
  case "$choice" in
    0) exit 0 ;;
    a|all) requested=--all ;;
    *)
      index=1
      for id do
        if [ "$choice" = "$index" ]; then requested=$id; break; fi
        index=$((index + 1))
      done
      ;;
  esac
fi

if [ "$requested" != --all ]; then
  found=false
  for id do
    if [ "$requested" = "$id" ]; then found=true; break; fi
  done
  if [ "$found" = false ]; then
    printf '목록에 있는 펫 ID 또는 메뉴 번호를 선택해 주세요.\n' >&2
    exit 1
  fi
  set -- "$requested"
fi

for id do
  for file in pet.json spritesheet.png; do
    if [ ! -f "$repo_dir/pets/$id/$file" ]; then
      printf '설치 파일이 없습니다: %s\n' "$repo_dir/pets/$id/$file" >&2
      exit 1
    fi
  done
done
mkdir -p "$pets_dir"
for id do install_pet "$id"; done

printf '\nCodex의 Settings → Pets에서 목록을 새로고침하고 설치한 새알심을 선택하세요.\n'
