---
name: wuwa-cube-pets
description: Wuwa Tappo의 새알심(Cube) 원본 에셋으로 Codex Desktop 펫을 추가하거나 수정한다. 에셋 확보, v1 스프라이트 제작, 애니메이션 WebP, 통합 설치 메뉴, README 갱신과 기여 PR 준비에 사용한다. ChatGPT Work Pets나 새 캐릭터 그림 생성에는 사용하지 않는다.
---

# Wuwa 새알심 펫 제작

대상 프로젝트는 [wuwa-cube-codex-pets](https://github.com/NARARIA03/wuwa-cube-codex-pets)다. 사용자가 지정한 체크아웃과 현재 파일을 우선하고, 요청한 단계만 수행한다. README 수정만 요청받았다면 에셋을 다시 만들지 않는다.

## 먼저 확인할 것

- 현재 `README.md`, `install.sh`, 기존 `pets/*/pet.json`, Git 변경 상태와 remote를 읽는다. 기여 작업이면 저장소의 `CONTRIBUTING.md`도 읽는다.
- 표시 이름은 `<한글 이름> 새알심`, ID와 폴더 이름은 `<영문 이름>-cube`다. 폴더와 매니페스트 ID는 서로 일치해야 한다.
- 이미 추출된 원본 PNG가 있으면 재사용한다. 새로 확보할 때는 [에셋 추출 안내](references/asset-source.md)를 읽는다. 캐릭터 이름뿐 아니라 Cube 시리즈 외형도 확인한다.
- `LICENSE.md`와 README의 `Source & Rights`, `Credits`는 사용자가 별도로 요청하지 않는 한 유지한다. 캐릭터 추가 때 권리 고지에 이름을 덧붙이지 않는다.

## 원본에서 펫 만들기

머리 두 장(`head1.png`, `head2.png`)과 손·몸 세 장(`body1.png`~`body3.png`)의 원본 투명 PNG를 사용한다. 원본 눈·손 동작의 조합만으로 구성하며, 새 포즈를 그리거나 GIF에서 프레임을 복원하지 않는다.

기존 패키지는 **v1** 형식이다. 8열 × 9행, 셀 `192 × 208`, 전체 `1536 × 1872` PNG RGBA이며 사용 프레임은 57개다. 행 순서는 `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, `review`다. 달리기·점프 상태도 원본 눈·손 동작을 재사용한다. v2나 시선 추적 프레임으로 임의 변경하지 않는다.

빌더는 기존과 같은 560 × 560 원본 레이어 구성을 대상으로 한다. 몸 위에 머리를 합성하고 192 × 192로 LANCZOS 축소한 뒤, 192 × 208 셀의 `(0, 8)`에 배치한다. 레이어 구성·크기·정렬이 다르면 먼저 원본과 비교하고 변환을 조정한다. 크기만 강제로 맞추지 않는다.

```sh
uv run --with pillow python /path/to/wuwa-cube-pets/scripts/build_cube_pet.py \
  --source /path/to/source \
  --id example-cube \
  --name '캐릭터 새알심' \
  --output /path/to/work/generated-example
```

`/path/to/wuwa-cube-pets`는 이 스킬 폴더로 바꾼다. Pillow와 `cwebp`, `webpmux`가 필요하다. 출력은 새 폴더여야 하며 기존 결과를 덮어쓰지 않는다. 생성물은 `pets/<id>/pet.json`, `pets/<id>/spritesheet.png`, `docs/<id>/idle.webp`, `docs/<id>/running.webp` 네 파일이다.

미리보기는 항상 **원본 PNG에서 만든 무손실 애니메이션 WebP**다. `cwebp -lossless -exact`와 `webpmux`를 사용한다. idle은 3프레임(500/280/320ms), running은 6프레임(120/120/120/120/120/220ms), 무한 반복이다. 빌더는 생성된 시트와 WebP를 다시 열어 RGBA·프레임 수·재생 시간을 검사한다.

## 저장소와 README 반영

검증한 네 파일을 동일한 상대 경로로 저장소에 추가한다. 기존 캐릭터 수정 요청이 아니라면 같은 ID를 덮어쓰지 않는다. 원본 다운로드, 추출 도구, 설치 실행 파일, 중간 프레임과 검증 기록은 Git에 넣지 않는다.

`install.sh`는 `pets/*/pet.json`을 자동 탐색한다. 새 캐릭터마다 별도 스크립트를 만들거나 메뉴를 하드코딩하지 않는다. 단일·전체 설치, 목록, 취소, 기존 설치 건너뛰기와 `CODEX_HOME` 지원을 유지한다.

README에서 서로 맞춰 갱신할 곳은 다음과 같다.

1. **Preview**: 한글 이름만 적은 행과 눈 깜빡임·손 동작 WebP 두 개. `<img>` 크기는 각각 `192 × 208`. GIF, Design 섹션, contact sheet, 영어 이름 병기를 추가하지 않는다.
2. **Install**: 새 ID로 실행할 수 있는 개별 설치 예시와 `펫 ID | Codex 표시 이름` 표. `--all`, `--list`, 메뉴 사용법은 유지한다.
3. **직접 설치하기**: 현재 `pets/` 목록과 같은 파일트리를 작성하고, 각 폴더에 `pet.json`과 `spritesheet.png`를 표시한다.

소개문에 현재 지원 캐릭터를 나열하지 않는다. 다른 사람의 README·LICENSE 참고 링크나 삭제된 WebP 가장자리 설명을 다시 넣지 않는다.

## 확인과 PR 공유

- 셀 경계·원본 레이어 정렬·반투명 가장자리를 밝은 배경과 어두운 배경에서 본다. 두 WebP가 움직이고 깜빡임과 손 동작이 구분되는지 확인한다.
- 설치는 임시 `CODEX_HOME`에서 확인한다. 실제 사용자 펫 폴더에 시험 설치하지 않는다. 실제 Codex 앱 확인 여부는 별도로 보고한다.
- `git diff --check`, README 로컬 이미지 경로, 새 ID의 목록 노출과 설치 파일을 확인한다. 검증용 테스트 코드나 contact sheet를 배포 저장소에 추가하지 않는다.
- 다른 기여자는 fork의 `add/<id>` 브랜치에서 작업하고 원본 저장소의 `main`을 대상으로 PR을 보낸다. PR에는 캐릭터, 공식 출처·role/skin ID, 정렬 변경 여부, **두 WebP**, 검증 결과와 앱 확인 여부를 포함한다. 저장소의 PR 템플릿을 사용한다.
- PR 이미지에는 fork의 **커밋 SHA를 포함한 raw URL**을 사용한다. 로컬 절대 경로나 아직 main에 없는 파일의 main URL을 공유하지 않는다.
- Codex가 작성하는 커밋에는 항상 `Co-Authored-By: GPT <version> <codex@openai.com>` 트레일러를 넣는다. `<version>`은 확인된 실제 모델 버전으로 바꾼다(예: `GPT 6`). 커밋 제목은 한국어를 기본으로 하며 `feat:` 등의 접두사는 필수가 아니다.
- 게시 전 로그인 계정·remote·변경 파일을 확인한다. PR 준비 요청은 자동 병합이나 main 직접 푸시 허가가 아니다. 사용자가 지정한 공유 방식과 기존 권한 범위 안에서 진행하고 PR URL을 돌려준다.
