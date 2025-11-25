import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import re

# ==========================================
# ⚙️ 설정 (Configuration)
# ==========================================
POSTS_DIR = Path("posts")
README_FILE = Path("README.md")

# ==========================================
# 📝 섹시한 템플릿 정의 (Templates)
# ==========================================

# 1. Computer Science (근본 지식)
TEMPLATE_CS = """---
title: "{title}"
date: "{date}"
category: "Computer Science"
tags: [{user_input}]
description: "Deep dive into CS fundamentals."
---

# 🏛️ {title}

## 📌 Abstract (핵심 요약)
> 

## 🔍 Deep Dive (상세 분석)
### 1. Mechanism (동작 원리)
<!-- 내부 동작 방식을 설명 -->

### 2. Key Concepts
- **Concept A:** - **Concept B:** ## ⚖️ Comparison
| Feature | {user_input} | Others |
| :--- | :--- | :--- |
| **Pros** | | |
| **Cons** | | |

## 📚 Reference
"""

# 2. Language & Framework (구현 기술)
TEMPLATE_LANG = """---
title: "{title}"
date: "{date}"
category: "Language & Framework"
tags: [{user_input}]
description: "Practical usage of {user_input}."
---

# 🛠️ {title}

## 🎯 Goal (목표)
<!-- 무엇을 구현하기 위해 학습했는가? -->

## 💻 Implementation (구현 과정)
### Step 1. Setup
```bash
# Command here
```

### Step 2. Code Snippet
```javascript
// Code here
```

## 💡 Best Practices
- 현업에서는 주로 이렇게 사용함:
- 주의할 점 (Gotchas): 
"""

# 3. Infrastructure (인프라/DevOps)
TEMPLATE_INFRA = """---
title: "{title}"
date: "{date}"
category: "Infrastructure"
tags: [{user_input}, DevOps]
description: "Infrastructure as Code and Deployment."
---

# ☁️ {title}

## 🏗️ Topology (구조도)
<!-- Mermaid 다이어그램 혹은 텍스트 설명 -->
```mermaid
graph TD;
    Client-->LoadBalancer;
    LoadBalancer-->Server;
```

## ⚙️ Configuration (설정)
> **File:** `config.yaml`
```yaml
# 설정 내용
```

## 🚀 Deployment Command
```bash
# 배포 명령어
```

## ⚠️ Check Point
- 보안 그룹(Security Group) 확인했는가?
- 환경 변수(Env Var) 설정했는가?
"""

# 4. Architecture (설계/디자인패턴)
TEMPLATE_ARCH = """---
title: "{title}"
date: "{date}"
category: "Architecture"
tags: [{user_input}, DesignPattern]
description: "System Design and Architecture Decisions."
---

# 📐 {title}

## 🧐 Context (배경)
<!-- 왜 이런 설계가 필요한가? -->

## 🎨 Diagram (설계도)
<!-- 시스템의 구조를 시각화 -->

## ⚖️ Decision Records (ADR)
### Alternative A vs Alternative B
- **선택한 방식:** - **이유:** - **Trade-off:** (무엇을 얻고 무엇을 잃었는가)

## 🎓 Conclusion
"""

# 5. Problem Solving (알고리즘)
TEMPLATE_PS = """---
title: "{title}"
date: "{date}"
category: "Problem Solving"
tags: [{user_input}, Algorithm]
description: "Algorithm solution and strategy."
---

# 🧠 {title}

## 🔗 Problem Info
- **Source:** {user_input}
- **Level:** ## 💡 Strategy (접근법)
<!-- 핵심 아이디어 -->

## 💻 Solution Code
```python
# Code
```

## ⏱️ Complexity
- **Time:** O()
- **Space:** O()
"""

# 6. Troubleshooting (에러 해결 - 중요!)
TEMPLATE_TS = """---
title: "{title}"
date: "{date}"
category: "Troubleshooting"
tags: [{user_input}, Debugging]
description: "Root cause analysis and resolution."
---

# 🚨 {title}

## 💣 The Issue (현상)
> **Error Log:**
> `ExampleError: ...`

- **Environment:** {user_input}
- **When:** (언제 발생했는지)

## 🕵️‍♂️ Root Cause Analysis (원인 분석)
1. **Hypothesis 1:** (가설)
2. **Verification:** (검증 결과)

## 💊 Solution (해결책)
```bash
# Final fix command or code
```

## 📝 Lesson Learned (교훈)
- 다시는 같은 실수를 반복하지 않기 위해:
"""

# 7. Review & Retrospect (회고/인사이트)
TEMPLATE_REVIEW = """---
title: "{title}"
date: "{date}"
category: "Review & Retrospect"
tags: [{user_input}, Insight]
description: "Retrospective and Thoughts."
---

# 📝 {title}

## 📅 Summary
<!-- 프로젝트/기간/이벤트 요약 -->

## 🌟 Key Takeaways (배운 점)
1. **Keep (좋았던 점):** 2. **Problem (아쉬웠던 점):** 3. **Try (시도할 점):** ## 💬 Conclusion
"""

# ==========================================
# 🧠 로직: 스마트 매핑 (Smart Mapping)
# ==========================================

def get_template_and_category(user_input):
    """사용자 입력(user_input)을 분석해 대분류 카테고리와 템플릿을 반환"""
    keyword = user_input.lower()

    # 1. Problem Solving
    if any(k in keyword for k in ['algo', 'boj', 'leet', 'code', 'ps', '백준', '프로그래머스']):
        return "Problem Solving", TEMPLATE_PS

    # 2. Troubleshooting
    if any(k in keyword for k in ['error', 'fix', 'debug', 'fail', 'issue', '에러', '버그', '트러블']):
        return "Troubleshooting", TEMPLATE_TS

    # 3. Infrastructure
    if any(k in keyword for k in ['docker', 'aws', 'k8s', 'jenkins', 'ci', 'cd', 'nginx', 'cloud', 'linux', 'server']):
        return "Infrastructure", TEMPLATE_INFRA

    # 4. Architecture
    if any(k in keyword for k in ['archi', 'design', 'pattern', 'msa', 'ddd', 'system', 'clean', '설계']):
        return "Architecture", TEMPLATE_ARCH

    # 5. Computer Science
    if any(k in keyword for k in ['cs', 'os', 'net', 'db', 'data', 'struct', 'algorithm-theory']):
        return "Computer Science", TEMPLATE_CS
    
    # 6. Review & Retrospect
    if any(k in keyword for k in ['review', 'retro', 'diary', 'log', '회고', '후기', '일기']):
        return "Review & Retrospect", TEMPLATE_REVIEW

    # 7. 기본값: Language & Framework (Spring, React, Next 등 대부분의 기술)
    return "Language & Framework", TEMPLATE_LANG


def slugify(text):
    return text.strip().replace(" ", "-").replace("/", "-")

def create_post(title, user_category_input):
    if not POSTS_DIR.exists():
        POSTS_DIR.mkdir()

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{slugify(title)}.md"
    filepath = POSTS_DIR / filename

    if filepath.exists():
        print(f"⚠️  이미 존재하는 파일입니다: {filename}")
        return

    # 스마트 매핑 실행
    category_name, selected_template = get_template_and_category(user_category_input)

    content = selected_template.format(
        title=title,
        date=today,
        user_input=user_category_input  # 태그용
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅  [{category_name}] 분류로 생성 완료: {filepath}")

def parse_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    
    data = {}
    yaml_text = match.group(1)
    for line in yaml_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    
    data['filename'] = file_path.name
    return data

def update_readme():
    # 🚀 수정됨: posts 폴더가 없어도 README를 생성하도록 로직 변경
    posts = []
    if POSTS_DIR.exists():
        for file in POSTS_DIR.glob("*.md"):
            meta = parse_frontmatter(file)
            if meta:
                posts.append(meta)

    # 정의된 순서대로 정렬하기 위한 리스트
    ORDERED_CATEGORIES = [
        "Computer Science",
        "Language & Framework",
        "Infrastructure",
        "Architecture",
        "Problem Solving",
        "Troubleshooting",
        "Review & Retrospect"
    ]

    grouped_posts = {cat: [] for cat in ORDERED_CATEGORIES}
    
    for post in posts:
        cat = post.get('category', 'Uncategorized')
        if cat not in grouped_posts:
            grouped_posts[cat] = [] # 정의되지 않은 카테고리 대비
        grouped_posts[cat].append(post)

    # README 헤더 (사용법 토글 적용)
    header = """# 🧠 Engineering Knowledge Base

> *"The goal of software architecture is to minimize the human resources required to build and maintain the required system."* - Robert C. Martin

현업 엔지니어링 관점(Engineering Layer)으로 정리된 학습 저장소입니다.

<details>
<summary>🚀 <strong>How to use (Click to expand)</strong></summary>

<br>

이 레포지토리는 `create.py` 스크립트로 관리됩니다. (키워드 자동 감지)

- **알고리즘 (Problem Solving)**: `python create.py "문제이름" -c Algo`
- **에러 해결 (Troubleshooting)**: `python create.py "에러메시지" -c Error`
- **CS 지식 (Computer Science)**: `python create.py "개념이름" -c CS`
- **인프라 (Infrastructure)**: `python create.py "주제" -c AWS`
- **아키텍처 (Architecture)**: `python create.py "주제" -c Design`
- **회고 (Review)**: `python create.py "회고" -c Review`
- **일반 개발 (Language & Framework)**: `python create.py "주제" -c React`
- **목차 갱신**: `python create.py --update`

</details>

---

## 🧭 Navigation
"""
    
    body = ""
    total_count = 0

    # 정의된 순서 + 그 외 카테고리 순으로 출력
    for cat in ORDERED_CATEGORIES + [k for k in grouped_posts.keys() if k not in ORDERED_CATEGORIES]:
        post_list = grouped_posts.get(cat, [])
        if not post_list:
            continue
        
        total_count += len(post_list)
        # 이모지 매핑
        icon = "📂"
        if cat == "Computer Science": icon = "🏛️"
        elif cat == "Language & Framework": icon = "🛠️"
        elif cat == "Infrastructure": icon = "☁️"
        elif cat == "Architecture": icon = "📐"
        elif cat == "Problem Solving": icon = "🧠"
        elif cat == "Troubleshooting": icon = "🚨"
        elif cat == "Review & Retrospect": icon = "📝"

        body += f"### {icon} {cat}\n\n"
        
        # 최신순 정렬
        sorted_posts = sorted(post_list, key=lambda x: x.get('date', ''), reverse=True)
        
        for post in sorted_posts:
            date = post.get('date', 'N/A')
            title = post.get('title', 'No Title')
            tags = post.get('tags', '').replace("[", "").replace("]", "")
            link = f"posts/{post['filename']}"
            
            # 태그 뱃지처럼 보이게
            tag_str = f" `#{tags}`" if tags else ""
            
            body += f"- `{date}` [{title}]({link}){tag_str}\n"
        body += "\n"

    stats = f"\nTotal Artifacts: **{total_count}**\n\n--- \n"
    
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(header + stats + body)
    
    print("🔄  README.md 구조화 업데이트 완료 (사용법 포함)!")

def main():
    parser = argparse.ArgumentParser(description="Engineering Log Generator")
    parser.add_argument("title", nargs="?", help="Document Title")
    parser.add_argument("-c", "--category", default="General", help="Keyword (e.g. NextJS, AWS, Error, Design)")
    parser.add_argument("--update", action="store_true", help="Update README only")

    args = parser.parse_args()

    if args.update or not args.title:
        update_readme()
    else:
        create_post(args.title, args.category)
        update_readme()

if __name__ == "__main__":
    main()