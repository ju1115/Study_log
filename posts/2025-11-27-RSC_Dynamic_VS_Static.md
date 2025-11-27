---
title: "RSC_Dynamic_VS_Static"
date: "2025-11-27"
category: "Language & Framework"
tags: [Next.js, RSC, AppRouter, Optimization]
description: "Next.js App Router가 RSC를 Static(정적) 또는 Dynamic(동적)으로 자동 분류하는 기준과 제어 방법 정리."
---

# 🛠️ `RSC_Dynamic_VS_Static`

## 🎯 Goal (목표)

Next.js App Router가 개발자의 코드(API 사용 패턴)를 분석하여 페이지를 **Static(빌드 시점 생성)**으로 처리할지 **Dynamic(요청 시점 생성)**으로 처리할지 결정하는 **자동 분류 메커니즘**을 이해한다. 이를 통해 의도적인 렌더링 전략 수립 능력을 기른다.

## 💻 Implementation (구현 과정)

### Step 1. Setup (확인 방법)

개발 모드(`dev`)에서는 모든 페이지가 Dynamic처럼 동작하므로, 실제 분류 결과를 확인하려면 **빌드**를 수행해야 한다.

```bash
# 프로젝트 빌드 실행
npm run build

# [출력 결과 해석]
# ○  (Static)  : 정적 페이지 (SSG) - 빌드 시점에 HTML 생성됨
# λ  (Dynamic) : 동적 페이지 (SSR) - 요청 올 때마다 서버에서 생성됨
```

### Step 2. Code Snippet

#### 1. Static Rendering (기본값 - Default)

별다른 설정이 없거나, 캐시 된 데이터를 사용하면 무조건 Static으로 분류된다.

```tsx
// app/blog/page.tsx
// 외부 데이터가 없거나, 기본 fetch(캐시됨)를 사용함 -> "○ Static"
export default async function BlogPage() {
  // 'force-cache'가 기본값 (빌드 시 1회 요청 후 결과 저장)
  const res = await fetch(
    "[https://api.example.com/posts](https://api.example.com/posts)"
  );
  const posts = await res.json();

  return (
    <div>
      {posts.map((post) => (
        <h2 key={post.id}>{post.title}</h2>
      ))}
    </div>
  );
}
```

#### 2. Dynamic Rendering (Opt-out)

**Dynamic API**를 사용하거나 캐시를 끄는 옵션을 주면 Dynamic으로 자동 전환된다.

```tsx
// app/dashboard/page.tsx
import { cookies } from "next/headers";

export default async function DashboardPage() {
  // [Trigger 1] Dynamic Functions 사용 (cookies, headers, searchParams)
  const cookieStore = cookies();
  const token = cookieStore.get("token");

  // [Trigger 2] No-Store Fetch 사용
  const res = await fetch(
    "[https://api.example.com/user](https://api.example.com/user)",
    {
      cache: "no-store", // "저장하지 마 = 매번 새로 가져와"
    }
  );

  return <div>실시간 유저 정보: {res.name}</div>;
}
```

## 💡 Best Practices

- **현업에서는 주로 이렇게 사용함:**

  - **Static First:** 가능한 모든 페이지는 Static으로 둔다. (마케팅 페이지, 블로그, 공지사항 등). 빌드된 HTML을 CDN에서 서빙하므로 속도가 가장 빠르다.
  - **부분 Dynamic:** 페이지 전체를 Dynamic으로 만들지 않고, 정적인 껍데기(Layout)는 Static으로 두고, 실시간 데이터가 필요한 부분만 **Client Component**로 분리하거나 **Suspense**로 감싸서 스트리밍한다.
  - **강제 설정:** 코드로 판단이 애매할 경우 `export const dynamic = 'force-dynamic'` 코드를 상단에 추가하여 명시적으로 SSR 모드를 켠다.

- **주의할 점 (Gotchas):**
  - **SearchParams:** 페이지 컴포넌트에서 `props.searchParams`(쿼리 스트링)를 사용하는 순간, 그 페이지는 즉시 **Dynamic**으로 변경된다. (쿼리는 사용자가 접속해야 알 수 있기 때문)
  - **Layout 오염:** 최상위 `layout.tsx`에서 `cookies()`나 `headers()`를 사용하면, 그 하위의 **모든 페이지**가 강제로 Dynamic 렌더링으로 바뀌어버린다. (Static 최적화 포기)
