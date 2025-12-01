---
title: "Figma Design System Setup for Developers"
date: "2025-11-28"
category: "Design"
tags: [Figma, DesignSystem, TailwindCSS, Workflow]
description: "개발 효율성을 높이는 피그마 디자인 시스템 구축 및 핸드오프 전략 (Free Plan 대응)"
---

# 🎨 `Figma_Style`

## 🎯 Design Goal (목표)

> **"개발 가능한" 디자인 시스템 구축**

- Next.js + Tailwind CSS (v4) 환경으로 매끄럽게 연결되는 색상, 타이포그래피, 그림자 체계 수립.
- 피그마 무료 플랜(Free Plan)의 한계를 우회하여, 현업 수준의 다크모드 대응 전략 마련.
- 수작업(노가다)을 최소화하는 플러그인 활용 워크플로우 정립.

## 🖼️ Prototype (Figma)

- **Link:** [Figma 보러가기](https://www.figma.com/design/fEtPeO4f1EG5UagoQ51Tm1/portfolio?node-id=0-1&p=f&t=hgRl8iDZE9lahZZu-0)
  ![Mockup](Your_Image_Path)

## 🎨 Design System Strategy

### 1. Color System (Dark Mode 대응)

- **Naming (Slash Rule):** `Base/White`, `Gray/50`~`950`, `Emerald/500`
- **Code:** Tailwind v4의 **OKLCH** 포맷을 사용하여 넓은 색역 지원.
- **Dark Mode:** 피그마에서는 Light 모드만 스타일로 정의하고, 다크모드는 `globals.css`의 `@variant`와 `dark:` 클래스로 제어.

### 2. Typography System (Text Styles)

- **Naming Strategy:** 불필요한 꼬리표 제거 & 데스크탑 기준.
  - 제목: `Heading/H1` (Bold 속성 포함)
  - 본문: `Body/1` (기본), `Body/1/Bold` (강조형이 필요할 때만 추가)
- **Responsive:** 피그마에는 Desktop 사이즈만 등록하고, Mobile은 Tailwind 유틸리티(`text-sm` 등)로 대응하는 **Mobile-First** 전략 사용.

### 3. Effect System (Shadows)

- **Naming:** `Shadow/md`, `Shadow/lg`, `Shadow/2xl` (Tailwind 기본 등급과 매칭)
- **Detail:** 자연스러운 깊이감을 위해 **Layered Shadow(2중 그림자)** 기법 사용.

### 4. Variables vs Styles

- **결정:** **Styles 사용** (Free Plan 효율성 최적화)
- **이유:** 무료 버전의 Variable Mode(테마 자동 전환) 제한을 우회하고, `Styler` 플러그인과의 호환성을 위해 Style로 관리.

## 🔄 Workflow (작업 순서)

**Step 1. 팔레트 및 스타일 준비 (Batch Rename)**

- **Color:** 사각형 나열 후 `Cmd + R`로 `Gray/$n00` 등 일괄 변경.
- **Text:** 텍스트 나열 후 `Desktop/Heading/H1` 등 규칙에 맞춰 네이밍.
- **Shadow:** `Shadow/md` 등으로 네이밍.

**Step 2. 스타일 자동 등록 (Automation)**

- **Plugin:** `Styler` 활용.
- 전체 레이어(Color, Text, Effect) 선택 후 "Generate Styles" 클릭 → 1초 만에 등록 완료.

**Step 3. 개발 핸드오프 (Handoff)**

- **추출:** 플러그인(`Export Styles to CSS Variables`) 또는 피그마 Inspect 패널 활용.
- **매핑:** 추출된 값을 Tailwind v4 문법(`--color-*`, `--text-*`)에 맞춰 `globals.css`에 이식.
- **검증:** `npm run dev` 후 다크모드 및 폰트 적용 확인.

## 💻 Code Implementation (Tailwind v4)

피그마의 모든 스타일(Color, Text, Shadow)을 `app/globals.css`에 통합한 최종 코드.

```css
/* 1. 폰트 CDN Import */
@import url("[https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css](https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css)");

@import "tailwindcss";

@theme {
  /* ✅ 2. Font Family */
  --font-pretendard: "Pretendard", sans-serif;

  /* ✅ 3. Color System (OKLCH) */
  --color-emerald-500: oklch(69.59% 0.1491 162.47deg);
  --color-base-white: oklch(100% 0 none);

  --color-gray-950: oklch(12.96% 0.0274 261.69deg);
  --color-gray-900: oklch(21.01% 0.0318 264.67deg);
  --color-gray-800: oklch(27.81% 0.0296 256.85deg);
  --color-gray-700: oklch(37.29% 0.0306 259.73deg);
  --color-gray-600: oklch(44.61% 0.0263 256.8deg);
  --color-gray-500: oklch(55.1% 0.0233 264.37deg);
  --color-gray-400: oklch(71.37% 0.0191 261.33deg);
  --color-gray-300: oklch(87.17% 0.0093 258.36deg);
  --color-gray-200: oklch(92.76% 0.0058 264.6deg);
  --color-gray-100: oklch(96.7% 0.0028 264.7deg);
  --color-gray-50: oklch(98.46% 0.0017 247.73deg);

  /* Semantic Alias */
  --color-background: var(--color-base-white);
  --color-foreground: var(--color-gray-900);

  /* ✅ 4. Typography System (Rem & Line Height) */
  /* Heading */
  --text-h1: 3.75rem; /* 60px */
  --text-h1--line-height: 1.2;
  --text-h1--font-weight: 700;

  --text-h2: 2.25rem; /* 36px */
  --text-h2--line-height: 1.1;
  --text-h2--font-weight: 600;

  --text-h3: 1.875rem; /* 30px */
  --text-h3--line-height: 1.2;
  --text-h3--font-weight: 600;

  /* Subtitle & Body */
  --text-subtitle: 1.25rem;
  --text-subtitle--line-height: 1.4;
  --text-subtitle--font-weight: 400;

  --text-body-1: 1.125rem; /* 18px */
  --text-body-1--line-height: 1.55;
  --text-body-1--font-weight: 400;

  --text-body-2: 1rem; /* 16px */
  --text-body-2--line-height: 1.5;
  --text-body-2--font-weight: 400;

  --text-body-3: 0.875rem; /* 14px */
  --text-body-3--line-height: 1.42;
  --text-body-3--font-weight: 400;

  /* ✅ 5. Shadow System (Layered) */
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);

  --shadow-lg: 0 10px 8px 0 rgb(0 0 0 / 0.04), 0 4px 3px 0 rgb(0 0 0 / 0.1);

  --shadow-2xl: 0 25px 25px 0 rgb(0 0 0 / 0.15);
}

/* Dark Mode Setup */
@variant dark (&:where(.dark, .dark *));

/* Global Reset */
body {
  background-color: var(--color-background);
  color: var(--color-foreground);
  font-family: var(--font-pretendard);
}
```

## 💬 Feedback & Iteration

- Insight: 디자인 툴의 최신 기능(Variables Mode)보다 현재 프로젝트 환경(Tailwind v4, Free Plan)에 맞는 실용적인 파이프라인을 구축함.

- Action Item: 이제 정의된 스타일과 컴포넌트 규칙을 바탕으로 Figma 화면 설계(Desktop First) 시작.
