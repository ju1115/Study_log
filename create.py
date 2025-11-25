import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import re

# ==========================================
# ⚙️ 사용자 설정 (User Configuration) - 🚨 본인 정보로 수정 필수
# ==========================================
MY_GITHUB_ID = "ju1115"               # 본인 깃허브 아이디
MY_ALGO_REPO = "Study_algorithm"      # 알고리즘 레포지토리 이름

# ==========================================
# ⚙️ 시스템 설정 (System Configuration)
# ==========================================
POSTS_DIR = Path("posts")
README_FILE = Path("README.md")

# ==========================================
# 📝 템플릿 정의 (Templates)
# ==========================================

# 1. Computer Science
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
- **Concept A:** - **Concept B:** 
## ⚖️ Comparison
| Feature | {user_input} | Others |
| :--- | :--- | :--- |
| **Pros** | | |
| **Cons** | | |

## 📚 Reference
"""

# 2. Language & Framework
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
```java
// Code here
```

## 💡 Best Practices
- 현업에서는 주로 이렇게 사용함:
- 주의할 점 (Gotchas): 
"""

# 3. Infrastructure
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

# 4. Architecture
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
- **선택한 방식:** 
- **이유:** 
- **Trade-off:** (무엇을 얻고 무엇을 잃었는가)

## 🎓 Conclusion
"""

# 5. Problem Solving (알고리즘) - 🚀 고급 검색 링크 적용
TEMPLATE_PS = """---
title: "{title}"
date: "{date}"
category: "Problem Solving"
tags: [{user_input}, Algorithm]
description: "Key strategy and lessons learned."
---

# 🧠 {title}

## 🔗 Problem Info
- **Problem:** [BOJ {prob_num}번]({prob_url})
- **My Solution:** [내 풀이 검색(Github)]({sol_url})
- **Level:** 
## 💡 Strategy (핵심 접근법)
<!-- 문제를 관통하는 핵심 아이디어와 자료구조 선정 이유 -->
- 

## 💻 Critical Snippet (핵심 로직)
<!-- 전체 코드가 아닌, 문제 해결의 결정적인 부분(5~10줄)만 발췌 -->
```java
// 여기에 핵심 로직만 붙여넣으세요
```

## 📝 Lesson Learned (오답 노트)
<!-- 시간 초과 원인, 몰랐던 개념, 실수했던 점 -->
- 
- 

## ⏱️ Complexity
- **Time:** O()
- **Space:** O()
"""

# 6. Troubleshooting
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

# 7. Review & Retrospect
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
### 1. **Keep (좋았던 점):** 
### 2. **Problem (아쉬웠던 점):** 
### 3. **Try (시도할 점):** 
## 💬 Conclusion
"""

# ==========================================
# 🧠 로직: 스마트 매핑 및 링크 생성
# ==========================================

def get_template_and_category(user_input):
    keyword = user_input.lower()
    if any(k in keyword for k in ['algo', 'boj', 'leet', 'code', 'ps', '백준', '프로그래머스']):
        return "Problem Solving", TEMPLATE_PS
    if any(k in keyword for k in ['error', 'fix', 'debug', 'fail', 'issue', '에러', '버그', '트러블']):
        return "Troubleshooting", TEMPLATE_TS
    if any(k in keyword for k in ['docker', 'aws', 'k8s', 'jenkins', 'ci', 'cd', 'nginx', 'cloud', 'linux', 'server']):
        return "Infrastructure", TEMPLATE_INFRA
    if any(k in keyword for k in ['archi', 'design', 'pattern', 'msa', 'ddd', 'system', 'clean', '설계']):
        return "Architecture", TEMPLATE_ARCH
    if any(k in keyword for k in ['cs', 'os', 'net', 'db', 'data', 'struct', 'algorithm-theory']):
        return "Computer Science", TEMPLATE_CS
    if any(k in keyword for k in ['review', 'retro', 'diary', 'log', '회고', '후기', '일기']):
        return "Review & Retrospect", TEMPLATE_REVIEW
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

    category_name, selected_template = get_template_and_category(user_category_input)

    context = {
        "title": title,
        "date": today,
        "user_input": user_category_input
    }

    # [알고리즘 전용] 문제 번호 추출 및 고급 검색 링크 생성
    if category_name == "Problem Solving":
        num_match = re.search(r'(\d+)', title)
        
        if num_match:
            prob_num = num_match.group(1)
            context["prob_num"] = prob_num
            context["prob_url"] = f"https://www.acmicpc.net/problem/{prob_num}"
            
            # 🚀 수정됨: Repo 필터 + Filename 필터 적용된 강력한 검색 링크
            # 형식: https://github.com/search?q=repo:아이디/레포+filename:번호&type=code
            search_query = f"repo:{MY_GITHUB_ID}/{MY_ALGO_REPO}+filename:{prob_num}"
            context["sol_url"] = f"https://github.com/search?q={search_query}&type=code"
            
            print(f"   🔍 고급 검색 링크 생성: {context['sol_url']}")
        else:
            context["prob_num"] = "???"
            context["prob_url"] = "#"
            context["sol_url"] = "#"

    try:
        content = selected_template.format(**context)
    except KeyError:
        content = selected_template.format(
            title=title, date=today, user_input=user_category_input,
            prob_num="?", prob_url="#", sol_url="#"
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
    posts = []
    if POSTS_DIR.exists():
        for file in POSTS_DIR.glob("*.md"):
            meta = parse_frontmatter(file)
            if meta:
                posts.append(meta)

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
            grouped_posts[cat] = []
        grouped_posts[cat].append(post)

    header = """# 🧠 Engineering Knowledge Base

> *"The goal of software architecture is to minimize the human resources required to build and maintain the required system."* - Robert C. Martin

현업 엔지니어링 관점(Engineering Layer)으로 정리된 학습 저장소입니다.

<details>
<summary>🚀 <strong>How to use (Click to expand)</strong></summary>

<br>

이 레포지토리는 `create.py` 스크립트로 관리됩니다. (키워드 자동 감지)

- **알고리즘**: `python create.py "백준 25757번 임스와 함께" -c Algo` (고급 검색 링크 자동생성!)
- **에러 해결**: `python create.py "에러메시지" -c Error`
- **CS 지식**: `python create.py "개념이름" -c CS`
- **인프라**: `python create.py "주제" -c AWS`
- **아키텍처**: `python create.py "주제" -c Design`
- **회고**: `python create.py "회고" -c Review`
- **일반 개발**: `python create.py "주제" -c React`
- **목차 갱신**: `python create.py --update`

</details>

---

## 🧭 Navigation
"""
    
    body = ""
    total_count = 0

    for cat in ORDERED_CATEGORIES + [k for k in grouped_posts.keys() if k not in ORDERED_CATEGORIES]:
        post_list = grouped_posts.get(cat, [])
        if not post_list:
            continue
        total_count += len(post_list)
        icon = "📂"
        if cat == "Computer Science": icon = "🏛️"
        elif cat == "Language & Framework": icon = "🛠️"
        elif cat == "Infrastructure": icon = "☁️"
        elif cat == "Architecture": icon = "📐"
        elif cat == "Problem Solving": icon = "🧠"
        elif cat == "Troubleshooting": icon = "🚨"
        elif cat == "Review & Retrospect": icon = "📝"

        body += f"### {icon} {cat}\n\n"
        sorted_posts = sorted(post_list, key=lambda x: x.get('date', ''), reverse=True)
        for post in sorted_posts:
            date = post.get('date', 'N/A')
            title = post.get('title', 'No Title')
            tags = post.get('tags', '').replace("[", "").replace("]", "")
            link = f"posts/{post['filename']}"
            tag_str = f" `#{tags}`" if tags else ""
            body += f"- `{date}` [{title}]({link}){tag_str}\n"
        body += "\n"

    stats = f"\nTotal Artifacts: **{total_count}**\n\n--- \n"
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(header + stats + body)
    
    print("🔄  README.md 구조화 업데이트 완료!")

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