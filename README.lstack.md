# LStack (LifeMashStack)

<mark>**LStack은 Lauren Tan의 pstack을 Codex에서 사용하도록 수정한 LifeMash 플러그인입니다.**</mark> 원본 플레이북을 유지하고 Codex 도구와 모델 설정을 연결합니다. 원본 설명은 [pstack README](pstack/README.md)에 있습니다.

## 설치

```bash
codex plugin marketplace add LifeMash-app/LStack
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

Astra는 자동으로 호출하지 않습니다. 메인 대화의 모델 설정은 실행할 때 결정하며, 플러그인은 메인 모델을 변경하지 않습니다.

역할별 설정은 `$CODEX_HOME/pstack-models.md`에서 읽으며 기본 위치는 `~/.codex/pstack-models.md`입니다. 파일이 없으면 [LifeMash 기본 설정](pstack/docs/harness/codex/pstack-models.md)을 복사합니다. 기존 파일은 유지하고, `$pstack:setup-pstack`으로 사용 가능한 모델과 추론 강도를 확인한 뒤 변경합니다. `모델@추론강도`를 쓰며 `auto`와 `inherit-parent`는 대화의 설정을 따릅니다. 자세한 연결은 [Codex 호환 지침](pstack/docs/harness/codex.md)에 있습니다.

## 과거 대화와 워크트리 확인

<mark>**`recall`, `reflect`, 작업 인계는 현재 작업 폴더의 Codex 기록을 조회합니다.**</mark> 활성 기록과 보관된 기록을 함께 찾고, 하위 에이전트 기록은 필요할 때 포함합니다. 다른 작업 폴더의 대화 본문은 읽지 않습니다. 워크트리 감사는 최근 작업 기록이 있으면 삭제 가능한 항목에서 제외하며, 직접 삭제하지 않습니다.

```bash
node pstack/docs/harness/codex/sessions.mjs --cwd "$PWD"
node pstack/docs/harness/codex/worktree-audit.mjs "$PWD"
```

압축 기록에는 Node 24.22 이상의 24.x 버전 또는 26.10 이상이 필요합니다. 기본 Node가 오래됐다면 위 명령의 `node`를 `npm exec --yes --package=node@24.22.1 -- node`로 바꿔 실행합니다. 시스템 Node를 변경하지 않습니다.

## pstack 업데이트 반영

<mark>**pstack의 변경은 원본 저장소에서 가져오고, Codex 기능은 PR #1143의 변경도 확인합니다.**</mark> 반영 기준 커밋은 [원본 기록](pstack/docs/harness/upstream.json)에 있습니다. PR #1143은 아직 병합 전이며, LStack은 해당 구현을 가져와 사용합니다. 모델 설정과 Astra 제한, 한국어 작성 규칙, 대화 모드, 추가 세 스킬은 유지합니다.

```bash
git fetch upstream main
git fetch upstream refs/pull/1143/head:refs/remotes/upstream/pr-1143
```

이전 반영 커밋부터의 pstack 변경을 비교해 적용한 뒤 아래 검증을 실행하고 원본 기록을 갱신합니다. 업데이트 확인은 유지보수 시 실행하며 자동 예약 작업을 설치하지 않습니다.

## 로컬 개발

```bash
node scripts/configure-lstack-codex.mjs --check
node scripts/generate-pstack-harness-trees.mjs --check
python3 -m unittest discover -s pstack/hooks/tests
node --test scripts/test/*.test.mjs
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
