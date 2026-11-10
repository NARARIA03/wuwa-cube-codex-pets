# Wuwa Cube Codex Pets

Wuwa Tappo의 **새알심(Cube)** 캐릭터를 Codex에서 사용할 수 있도록 정리한 비공식 커스텀 펫 모음입니다. 현재 **에이메스(Aemeath)**와 **치사(Chisa)**를 지원합니다.

Codex Dots를 활용해 Wuwa Tappo의 에셋을 언팩하고, 원본 눈 깜빡임과 손 동작을 Codex 펫 형식으로 구성했습니다.

## Preview

| 새알심 | 눈 깜빡임 | 손 동작 |
| --- | --- | --- |
| **에이메스**<br>Aemeath Cube | <img src="docs/aemeath-cube/idle.webp" alt="에이메스 새알심 눈 깜빡임" width="192" height="208"> | <img src="docs/aemeath-cube/running.webp" alt="에이메스 새알심 손 동작" width="192" height="208"> |
| **치사**<br>Chisa Cube | <img src="docs/chisa-cube/idle.webp" alt="치사 새알심 눈 깜빡임" width="192" height="208"> | <img src="docs/chisa-cube/running.webp" alt="치사 새알심 손 동작" width="192" height="208"> |

원본의 눈·손 동작을 9개 상태에 배치했습니다. `running`이나 `jumping` 상태에서도 이 동작을 사용하며, 별도의 달리기·점프 포즈나 시선 추적 프레임은 포함하지 않습니다.

## Install

로컬 커스텀 펫을 지원하는 Codex Desktop이 필요합니다. 아래 명령은 macOS / Linux 셸용입니다.

```sh
git clone https://github.com/NARARIA03/wuwa-cube-codex-pets.git
cd wuwa-cube-codex-pets
./install.sh
```

메뉴에서 캐릭터 번호를 선택하세요. `a`는 전체 설치, `0`은 취소입니다. 이미 설치된 펫은 덮어쓰지 않고 건너뜁니다.

펫 ID를 지정하면 메뉴 없이 설치할 수 있습니다.

```sh
./install.sh aemeath-cube
./install.sh chisa-cube
./install.sh --all
./install.sh --list
```

| 펫 ID | Codex 표시 이름 |
| --- | --- |
| `aemeath-cube` | 에이메스 새알심 |
| `chisa-cube` | 치사 새알심 |

기본 설치 위치는 `~/.codex/pets/<펫 ID>/`입니다. `CODEX_HOME`을 설정했다면 해당 경로의 `pets/<펫 ID>/`에 설치합니다.

설치 후 Codex의 **Settings → Pets**에서 목록을 새로고침하고 설치한 새알심을 선택하세요. 목록에 보이지 않으면 앱을 다시 실행해 주세요. 펫 표시 기능은 `/pet` 또는 **Show pet**으로 켤 수 있습니다. 일반적인 사용 방법은 [OpenAI 공식 Pets 안내](https://learn.chatgpt.com/docs/pets)를 참고하세요.

### 직접 설치하기

저장소에서 **Code → Download ZIP**으로 내려받아 압축을 풉니다. `pets` 안에서 원하는 캐릭터 폴더를 Codex 설정 경로의 `pets` 폴더에 복사하세요. 기존에 같은 이름의 펫이 있다면 먼저 백업해 주세요.

```text
~/.codex/pets/
├── aemeath-cube/
│   ├── pet.json
│   └── spritesheet.png
└── chisa-cube/
    ├── pet.json
    └── spritesheet.png
```

`CODEX_HOME`을 사용하는 경우 `~/.codex` 대신 해당 경로를 사용합니다. 제거할 때는 해당 캐릭터 폴더를 삭제하고 앱을 다시 실행하면 됩니다.

## Files

| 경로 | 용도 |
| --- | --- |
| `pets/<펫 ID>/pet.json` | 펫 이름과 스프라이트 경로 |
| `pets/<펫 ID>/spritesheet.png` | Codex용 투명 배경 스프라이트 시트 |
| `docs/<펫 ID>/idle.webp` | 눈 깜빡임 애니메이션 미리보기 |
| `docs/<펫 ID>/running.webp` | 손 동작 애니메이션 미리보기 |
| `install.sh` | 개별·전체 설치 메뉴 |
| `LICENSE.md` | 원작 및 에셋 권리 고지와 이용 안내 |

스프라이트는 **v1 형식**입니다: PNG RGBA, `1536 × 1872`, 8열 × 9행, 프레임당 `192 × 208`. 미리보기는 모두 무손실 애니메이션 WebP를 사용합니다.

새 캐릭터는 `pets/<펫 ID>/`에 `pet.json`과 `spritesheet.png`를 추가하면 설치 메뉴에 자동으로 나타납니다. 폴더 이름은 매니페스트의 `id`와 같아야 합니다.

## Source & Rights


이 패키지는 [Wuwa Tappo](https://download-wutheringwaves-wuwatappo.kurogames-global.com/download/kr/)의 에이메스·치사 에셋을 Codex Dots로 언팩하고, 원본 눈·손 동작을 Codex 펫 형식에 맞게 배치했습니다.

**[명조: 워더링 웨이브(Wuthering Waves)](https://wutheringwaves.kurogames.com/kr/), 에이메스·치사 및 이 패키지에 사용된 원본 캐릭터 디자인·이미지 에셋의 저작권과 모든 지적 재산권은 [Kuro Games](https://www.kurogames.com/)에 귀속됩니다.**

개인 Codex 환경을 위한 비공식 팬 패키지입니다. 원작 에셋의 이용에는 원 권리자의 약관과 권리가 적용되며, 자세한 내용은 [LICENSE.md](LICENSE.md)를 참고해 주세요.

## Credits

- 원작사: [Kuro Games 공식 사이트](https://www.kurogames.com/)
- 원작 게임: [명조: 워더링 웨이브 공식 사이트](https://wutheringwaves.kurogames.com/kr/)
- 에셋 출처: [Wuwa Tappo 공식 사이트](https://download-wutheringwaves-wuwatappo.kurogames-global.com/download/kr/)
- README 구성과 권리 고지 참고: [hyeonbungi/aemeath-codex-pet](https://github.com/hyeonbungi/aemeath-codex-pet), [참고 LICENSE](https://github.com/hyeonbungi/aemeath-codex-pet/blob/main/LICENSE.md)
