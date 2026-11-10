# 새알심 추가하기

새 캐릭터는 원본 레이어를 확보하고, 펫 파일 두 개와 WebP 미리보기 두 개를 만든 뒤 README를 갱신하는 방식으로 추가합니다. `LICENSE.md`와 README의 기존 권리 고지는 캐릭터 추가 때 수정하지 않습니다.

## Codex 스킬로 진행하기

이 저장소의 [wuwa-cube-pets 스킬](skills/wuwa-cube-pets/SKILL.md)에 제작부터 PR 준비까지의 흐름을 정리했습니다. Codex 없이도 아래 명령으로 제작할 수 있습니다.

스킬을 Codex에서 사용하려면 저장소 루트에서 다음 명령을 실행합니다. 같은 이름의 스킬이 이미 있다면 덮어쓰지 않으므로 기존 내용을 먼저 비교해 주세요.

```sh
skill_dir="${CODEX_HOME:-$HOME/.codex}/skills/wuwa-cube-pets"
mkdir -p "$(dirname "$skill_dir")"
if [ -e "$skill_dir" ] || [ -L "$skill_dir" ]; then
  printf '이미 설치된 스킬이 있습니다: %s\n' "$skill_dir"
else
  cp -R skills/wuwa-cube-pets "$skill_dir"
fi
```

사용 예시: `$wuwa-cube-pets를 사용해서 새 캐릭터의 새알심을 추가하고 PR을 준비해 주세요.`

## 1. 작업 브랜치와 원본 준비

이 저장소를 자신의 GitHub 계정으로 fork하고 clone한 뒤 작업 브랜치를 만듭니다. 아래 `example-cube`와 표시 이름은 추가하려는 캐릭터로 바꿔 주세요.

```sh
pet_id=example-cube
pet_name='캐릭터 새알심'
git switch -c "add/$pet_id"
```

[에셋 추출 안내](skills/wuwa-cube-pets/references/asset-source.md)를 따라 공식 Wuwa Tappo 카탈로그에서 Cube 시리즈와 원본 PNG를 확인합니다. 이미 추출한 원본이 있다면 재사용합니다.

필요한 레이어는 `head1.png`, `head2.png`, `body1.png`, `body2.png`, `body3.png`입니다. 원본 URL, `game_role_id`, skin ID와 확인 날짜를 기록해 주세요. 중간 작업은 Git에서 제외되는 `work/`에 둡니다.

## 2. 펫 데이터와 WebP 만들기

Python/Pillow와 WebP 도구의 `cwebp`, `webpmux`가 필요합니다. 아래 명령은 `uv`로 Pillow를 실행 환경에 준비합니다. macOS에서 WebP 도구가 없다면 Homebrew의 `webp` 패키지로 설치할 수 있습니다.

```sh
uv run --with pillow python skills/wuwa-cube-pets/scripts/build_cube_pet.py \
  --source work/tappo/source-SKIN_ID \
  --id "$pet_id" \
  --name "$pet_name" \
  --output "work/generated-$pet_id"
```

`source-SKIN_ID`는 실제 원본 폴더로 바꿉니다. 출력 폴더가 이미 있으면 새 경로를 사용하세요. 실패한 빌드의 중간 결과도 해당 작업 폴더에 남을 수 있습니다.

빌더는 560 × 560 원본 몸·머리를 합성하고 192 × 192로 줄인 뒤, 192 × 208 셀의 `(0, 8)` 위치에 배치합니다. 눈·손 조합을 기존 9개 상태에 맞춰 v1 시트에 넣습니다. 결과는 `1536 × 1872` PNG RGBA이며, 빈 셀을 포함한 72개 셀과 WebP 9프레임의 RGBA·재생 시간을 검사합니다.

미리보기는 PNG에서 직접 만든 무손실 애니메이션 WebP입니다. GIF나 새로 그린 포즈를 입력으로 사용하지 않습니다. 원본 레이어의 크기나 정렬 방식이 다르면 빌더에 맞춰 강제로 자르지 말고 변환을 먼저 검토해 주세요.

## 3. 저장소에 넣을 파일

생성 결과에서 다음 네 파일만 같은 위치로 옮깁니다.

```text
pets/<펫 ID>/
├── pet.json
└── spritesheet.png
docs/<펫 ID>/
├── idle.webp
└── running.webp
```

```sh
if [ -e "pets/$pet_id" ] || [ -L "pets/$pet_id" ] || [ -e "docs/$pet_id" ] || [ -L "docs/$pet_id" ]; then
  printf '같은 ID가 이미 있습니다. 기존 파일을 먼저 확인해 주세요.\n'
else
  cp -R "work/generated-$pet_id/pets/$pet_id" pets/
  cp -R "work/generated-$pet_id/docs/$pet_id" docs/
fi
```

폴더 이름과 `pet.json`의 `id`는 같아야 합니다. `install.sh`는 `pets/*/pet.json`을 자동 탐색하므로 캐릭터 추가만으로 설치 메뉴에 나타납니다. 캐릭터별 설치 스크립트는 만들지 않습니다.

## 4. README 갱신

아래 세 곳을 함께 갱신합니다.

| 위치 | 수정 내용 |
| --- | --- |
| Preview | 한글 이름과 눈 깜빡임·손 동작 WebP 두 개를 가진 행 추가 |
| Install | 개별 설치 명령 예시와 펫 ID·Codex 표시 이름 표 추가 |
| 직접 설치하기 | 현재 모든 펫 폴더 및 각 `pet.json`·`spritesheet.png`를 파일트리에 표시 |

Preview 행은 다음 형식을 사용합니다. 영어 이름을 덧붙이지 않고, 두 미리보기 모두 애니메이션 WebP로 둡니다.

```markdown
| **캐릭터명** | <img src="docs/example-cube/idle.webp" alt="캐릭터명 새알심 눈 깜빡임" width="192" height="208"> | <img src="docs/example-cube/running.webp" alt="캐릭터명 새알심 손 동작" width="192" height="208"> |
```

소개문의 지원 캐릭터 나열, Design 섹션, contact sheet, 외부 README·LICENSE 참고 크레딧은 추가하지 않습니다.

## 5. 확인하고 PR 보내기

밝은 배경과 어두운 배경에서 원본 정렬, 프레임 잘림, 반투명 가장자리를 확인합니다. 두 WebP를 열어 깜빡임과 손 동작이 실제로 재생되는지도 확인해 주세요.

설치는 실제 설정 폴더 대신 임시 경로에서 확인할 수 있습니다.

```sh
./install.sh --list
pet_check_dir=$(mktemp -d)
CODEX_HOME="$pet_check_dir" ./install.sh "$pet_id"
cmp "pets/$pet_id/pet.json" "$pet_check_dir/pets/$pet_id/pet.json"
cmp "pets/$pet_id/spritesheet.png" "$pet_check_dir/pets/$pet_id/spritesheet.png"
CODEX_HOME="$pet_check_dir" ./install.sh "$pet_id"
git diff --check
```

두 번째 설치는 이미 설치되었다는 메시지와 함께 건너뛰어야 합니다. 실제 Codex 앱에서 확인하지 않았다면 PR에 미확인으로 표시합니다. 테스트 코드·중간 이미지·원본 설치 파일은 커밋하지 않습니다.

로그인 계정과 `origin`이 자신의 fork인지 확인한 후 필요한 파일만 커밋하고 push합니다.

```sh
gh api user --jq .login
git remote -v
git add -- "pets/$pet_id" "docs/$pet_id" README.md
git commit -m "Add $pet_id"
git push -u origin "add/$pet_id"
```

Codex가 작성한 커밋에는 `Co-Authored-By: GPT <version> <codex@openai.com>` 트레일러를 반드시 넣습니다. `<version>`은 사용한 모델 버전으로 바꾸고, 제목과 빈 줄로 구분합니다. 예를 들어 GPT 6으로 작성했다면 다음 형식입니다. 직접 작성한 커밋에 사용하지 않은 도구의 기여 정보를 넣을 필요는 없습니다.

```text
새알심 캐릭터 추가

Co-Authored-By: GPT 6 <codex@openai.com>
```

GitHub에서 **base: `NARARIA03/wuwa-cube-codex-pets`의 `main`**, **head: 자신의 fork의 `add/<펫 ID>`**로 PR을 엽니다. 자동으로 표시되는 [PR 템플릿](.github/pull_request_template.md)에 출처, 두 WebP, 검증 결과를 적어 주세요.

PR의 미리보기 URL은 아래처럼 **자신의 fork와 커밋 SHA**를 사용합니다. `git rev-parse HEAD`로 SHA를 확인할 수 있습니다. 로컬 파일 경로나 아직 새 파일이 없는 원본 저장소의 main URL은 사용하지 않습니다.

```markdown
| 눈 깜빡임 | 손 동작 |
| --- | --- |
| <img src="https://raw.githubusercontent.com/ACCOUNT/wuwa-cube-codex-pets/COMMIT_SHA/docs/PET_ID/idle.webp" width="192" height="208" alt="눈 깜빡임"> | <img src="https://raw.githubusercontent.com/ACCOUNT/wuwa-cube-codex-pets/COMMIT_SHA/docs/PET_ID/running.webp" width="192" height="208" alt="손 동작"> |
```

CLI로 제출할 경우 템플릿을 `work/pr-body.md`에 복사해 작성하고 다음 명령을 사용합니다. `ACCOUNT`는 자신의 GitHub 계정으로 바꿉니다.

```sh
gh pr create --repo NARARIA03/wuwa-cube-codex-pets --base main \
  --head "ACCOUNT:add/$pet_id" --title "$pet_name 추가" --body-file work/pr-body.md
```

제출 후 생성된 PR URL을 공유하면 됩니다. 리뷰 중 수정은 같은 브랜치에 추가 커밋으로 반영합니다.
