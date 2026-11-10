# Wuwa Tappo 원본 에셋 확보

이 안내는 공식 배포 데이터에서 머리·몸 PNG를 확보하는 방법이다. 새로 다운로드하기 전에 보유한 원본을 확인한다. 저장소에는 완성된 펫과 WebP만 추가하고 다운로드·추출 자료는 `work/`에 둔다.

## 공개 카탈로그에서 찾기

2026-11-10에 [Wuwa Tappo 공식 사이트](https://download-wutheringwaves-wuwatappo.kurogames-global.com/download/kr/)와 공식 앱 데이터에서 확인한 경로다. 파일 URL의 UUID나 타임스탬프를 추측하지 않고 현재 설정의 `url`을 따라간다. HTTP 오류나 스키마 변경이 있으면 중단하고 공식 페이지·앱의 현재 경로를 확인한다.

아래 명령은 저장소 루트의 macOS/Linux 셸에서 실행한다. `curl`, `jq`가 필요하다.

```sh
set -eu
mkdir -p work/tappo
curl -fsSL 'https://api-wutheringwaves-wuwatappo.kurogames-global.com/api/common/activity-config' \
  -o work/tappo/config.json
tappo_host=$(jq -er '.data.assets_host' work/tappo/config.json)
curl -fsSL "$tappo_host/app/json-host/appearance_asset_host.json" -o work/tappo/asset-host.json
curl -fsSL "$(jq -er '.url' work/tappo/asset-host.json)" -o work/tappo/catalog.json
curl -fsSL "$tappo_host/app/json-host/dict_host.json" -o work/tappo/dict-host.json
curl -fsSL "$(jq -er '.url.kr' work/tappo/dict-host.json)" -o work/tappo/kr.json
curl -fsSL "$(jq -er '.url.en' work/tappo/dict-host.json)" -o work/tappo/en.json
```

`kr.json`과 `en.json`의 `character` 객체가 게임 캐릭터 ID와 이름을 연결한다. 다음은 치사를 검색하는 예시다. 다른 캐릭터는 이름을 바꾼다.

```sh
jq '.character | to_entries[] | select(.value == "치사")' work/tappo/kr.json
tappo_role_id=1508
jq --argjson role "$tappo_role_id" \
  '.character_skin | to_entries[] | select(.value.game_role_id == $role) | {skin_id: .key, data: .value}' \
  work/tappo/catalog.json
```

한 캐릭터에 여러 시리즈가 있다. `series` 번역에서 `1002`는 영어 `Cube, Cubic n Cubie`, 한국어 `데굴데굴 빙글빙글`로 확인했지만, **모양과 실제 레이어를 함께 확인해야 한다.** `character_skin`의 `url`은 완성 모습, `head1`, `head2`, `body1`~`body3`의 `url`은 개별 레이어다. 상대 URL 앞에 `tappo_host`를 붙여 원본을 확인한다.

초기 패키지에서 확인한 값은 다음과 같다. 이후 버전의 고정 규칙으로 취급하지 않는다.

| 캐릭터 | game_role_id | Cube skin ID |
| --- | --- | --- |
| 에이메스 | 1210 | 266 |
| 치사 | 1508 | 146 |

다음은 확인한 치사 skin ID로 다운로드하는 예시다. 새 캐릭터 작업에서는 해당 값을 바꾼다. 이 명령은 존재하는 출력 폴더를 덮어쓰지 않는다.

```sh
tappo_skin_id=146
source_dir="work/tappo/source-$tappo_skin_id"
mkdir "$source_dir"
jq -e --arg skin "$tappo_skin_id" '.character_skin[$skin]' work/tappo/catalog.json > "$source_dir/source.json"
for part in head1 head2 body1 body2 body3; do
  relative_url=$(jq -er --arg part "$part" '.[$part].url' "$source_dir/source.json")
  curl -fsSL "$tappo_host/$relative_url" -o "$source_dir/$part.png"
done
relative_url=$(jq -er '.url' "$source_dir/source.json")
curl -fsSL "$tappo_host/$relative_url" -o "$source_dir/full.png"
```

`source.json`의 role/skin 정보와 URL, 다운로드 날짜를 작업 기록에 남긴다. PR에는 이 출처 정보를 적되 원본 묶음이나 전체 카탈로그를 첨부하지 않는다.

## 설치 파일에서 확인해야 하는 경우

기존 작업에서는 공식 Windows 설치 파일의 내장 NSIS 패키지에서 Tappo 실행 파일을 꺼내고, Tauri에 포함된 Brotli 압축 프런트엔드 자산을 추출해 위 카탈로그 경로를 확인했다. 현재 공개 카탈로그만으로 필요한 PNG를 받을 수 있다면 이 과정을 반복할 필요는 없다.

공개 경로가 바뀌었다면 공식 배포 페이지의 최신 설치 파일과 앱 자산을 조사한다. 설치 파일을 실행할 필요는 없으며, 버전에 따라 달라지는 PE 위치·NSIS 오프셋·프런트엔드 파일명을 하드코딩하지 않는다. 외부 추출 도구를 사용한다면 먼저 소스와 동작을 확인하고 작업 폴더에 한정한다. 인증이나 접근 제한을 우회하지 않는다.

## 제작 전 확인

- 다섯 레이어가 모두 같은 560 × 560 투명 PNG인지 확인한다. 팔레트 PNG도 RGBA 변환 후 사용할 수 있다.
- `head1`과 `head2`가 눈 상태, `body1`~`body3`가 손 상태에 해당하는지 실제 이미지를 본다.
- 기존 조합은 몸을 먼저 그리고 머리를 위에 합성한다. 원본의 전체 캔버스를 유지하며 개별 레이어를 따로 자르거나 중심을 다시 맞추지 않는다.
- PNG의 반투명 가장자리를 보존한다. GIF 변환 결과를 원본으로 삼거나 알파를 흑백으로 바꾸지 않는다.
- 다른 캐릭터의 배치가 맞지 않으면 `offset_x`, `offset_y`, `my_offset_x`, `my_offset_y`와 실제 앱의 정렬을 조사한 뒤 수정 내용을 PR에 설명한다.
