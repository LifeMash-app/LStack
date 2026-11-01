# LStack (LifeMashStack)

<mark>**LStack은 Lauren Tan의 pstack을 Codex에서 사용하도록 수정한 LifeMash 플러그인입니다.**</mark> 원본 플레이북을 유지하고 Codex 도구와 모델 설정을 연결합니다. 원본 설명은 [pstack README](pstack/README.md)에 있습니다.

## 설치

```bash
codex plugin marketplace add LifeMash-hq/LStack
codex plugin add pstack@lifemash
```

설치 후 새 Codex 대화에서 스킬을 직접 호출합니다. 자동 실행 훅은 설치하지 않습니다. 원본 스킬 참조를 유지하기 위해 플러그인 식별자는 `pstack`, 표시 이름은 LStack을 사용합니다.

```text
$pstack:poteto-mode 이 작업의 관련 코드와 호출 순서를 조사해줘. 파일은 수정하지 마.
```

동일한 이름의 기존 스킬이 있으면 스킬 선택 목록에서 LStack의 항목을 선택합니다.

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
