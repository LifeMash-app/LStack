# LStack (LifeMashStack)

<mark>**LStack은 Lauren Tan의 pstack을 Codex에서 사용하도록 수정한 LifeMash 플러그인입니다.**</mark> 원본 플레이북을 유지하고 Codex 도구와 모델 설정을 연결합니다. 원본 설명은 [pstack README](pstack/README.md)에 있습니다.

## 설치

```bash
codex plugin marketplace add LifeMash-hq/LStack
codex plugin add pstack@lifemash
```

설치 후 새 Codex 대화에서 스킬을 직접 호출합니다. 원본 스킬 참조를 유지하기 위해 플러그인 식별자는 `pstack`, 표시 이름은 LStack을 사용합니다.

```text
$pstack:poteto-mode 이 작업의 관련 코드와 호출 순서를 조사해줘. 파일은 수정하지 마.
```

동일한 이름의 기존 스킬이 있으면 스킬 선택 목록에서 LStack의 항목을 선택합니다.

## 대화별 Poteto 모드 유지

<mark>**한 번 켜면 현재 대화에서 스킬 이름을 반복해서 입력하지 않아도 됩니다.**</mark> 기본 상태는 꺼짐입니다. 로컬 Codex에서 플러그인 훅을 사용하며, 최초 사용과 훅 정의 변경 시 `/hooks`에서 내용을 검토하고 신뢰해야 합니다.

| 동작 | 입력 |
| --- | --- |
| 켜기 | `poteto 모드 켜줘` |
| 끄기 | `poteto 모드 꺼줘` |
| 상태 확인 | `poteto 모드 상태` |

입력의 첫 줄을 위 문구로 작성합니다. 다음 줄부터 작업을 적으면 모드 변경과 작업 요청을 함께 처리합니다. 영어 입력은 `poteto mode on`, `poteto mode off`, `poteto mode status`를 사용합니다.

같은 대화를 재개하거나 압축해도 상태를 유지합니다. 새 대화, 대화 분기, `/clear` 후에는 꺼짐으로 시작합니다. 기존 `$pstack:poteto-mode 작업` 호출은 해당 요청에만 적용됩니다.

훅은 매 요청에 짧은 스킬 참조만 전달하고, 모델 호출이나 대화 기록 저장을 하지 않습니다. 모델과 권한 설정은 유지합니다. 클라우드에서 대화를 실행하는 환경은 로컬 플러그인 훅을 지원하지 않으므로 요청마다 스킬을 직접 호출합니다. [Codex 훅 지원 범위](https://learn.chatgpt.com/docs/hooks)

Codex CLI 0.166.0에서는 표준 Agent Plugins 형식의 훅을 로더가 제외합니다. LStack은 훅을 지원하는 `.codex-plugin/plugin.json`으로 설치합니다. Claude용 배포본을 생성하는 공통 매니페스트는 `pstack/plugin.template.json`에 보관합니다.

## 모델

| 작업 | 모델 | 추론 강도 |
| --- | --- | --- |
| 일반 조사와 구현 | GPT-6.1 Sol | medium |
| 설계와 독립 리뷰, 어려운 디버깅 | GPT-6.1 Sol | high |
| 명시적으로 요청한 특정 판단 | GPT-6 Astra | low |

Astra는 자동으로 호출하지 않습니다. 메인 대화의 모델 설정은 실행할 때 결정합니다. 플러그인은 메인 모델을 변경하지 않습니다. 역할별 설정과 도구 연결은 [Codex 호환 지침](pstack/docs/harness/codex.md)에 있습니다.

## 로컬 개발

```bash
node scripts/configure-lstack-codex.mjs --check
node scripts/generate-pstack-harness-trees.mjs --check
python3 -m unittest discover -s pstack/hooks/tests
codex plugin marketplace add "$PWD"
codex plugin add pstack@lifemash
```

스킬을 추가하거나 호환 지침 연결을 갱신할 때는 다음 명령을 실행합니다.

```bash
node scripts/configure-lstack-codex.mjs
node scripts/generate-pstack-harness-trees.mjs
```

GitHub 설치본을 갱신할 때는 마켓플레이스를 갱신하고 플러그인을 다시 설치합니다.

```bash
codex plugin marketplace upgrade lifemash
codex plugin remove pstack@lifemash
codex plugin add pstack@lifemash
```

## 출처

원본은 [cursor/plugins의 pstack](https://github.com/cursor/plugins/tree/main/pstack)입니다. 원본의 MIT 라이선스와 저작권 표기를 유지합니다.

`cursor-team-kit`에서 가져온 `deslop`, `control-cli`, `control-ui`도 함께 배포합니다. [Cursor의 MIT 라이선스](pstack/LICENSE-cursor-team-kit)를 포함하며, 세 스킬의 본문은 원본 그대로 유지합니다.
