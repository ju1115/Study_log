---
title: "githubpage를_위한_static_page_settings"
date: "2025-11-27"
category: "Infrastructure"
tags: [Git, DevOps, Next.js, GitHubActions]
description: "Next.js(App Router) 프로젝트를 GitHub Actions를 통해 GitHub Pages로 SSG 배포하기 위한 설정 및 파이프라인 정리."
---

# ☁️ `githubpage를_위한_static_page_settings`

## 🏗️ Topology (배포 파이프라인 구조도)

```mermaid
graph LR;
    Dev[Developer] -->|Git Push| Repo[GitHub Repository];
    Repo -->|Trigger| Actions[GitHub Actions Runner];
    subgraph CI_CD_Pipeline
        Actions -->|Install & Build| SSG[Static HTML Generation];
        SSG -->|Upload Artifact| GH_Pages[GitHub Pages Server];
    end
    Browser[User Browser] -->|Access (ju1115.github.io)| GH_Pages;
```

## ⚙️ Configuration (설정 파일)

### 1. Next.js 설정 (`next.config.mjs`)

> **Role:** Node.js 서버 없이 100% 정적 파일(HTML/CSS/JS)로 빌드하고, 이미지 최적화 기능을 비활성화함.

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // SSG 모드: 'out' 폴더에 정적 파일 생성
  output: "export",

  // GitHub Pages는 Next.js Image Optimization 서버를 지원하지 않으므로 끔
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
```

### 2. GitHub Actions 설정 (`.github/workflows/deploy.yml`)

> **Role:** 코드가 push 될 때마다 자동으로 빌드하고 GitHub Pages로 배포하는 파이프라인 정의.

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
      - name: Install dependencies
        run: npm ci
      - name: Build
        run: npm run build
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./out

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## 🚀 Deployment Command

터미널에서 설정 파일을 반영하고 GitHub로 전송하는 명령어.

```bash
# 1. 변경 사항 스테이징
git add .

# 2. 커밋 메시지 작성
git commit -m "chore: setup github actions for ssg deployment"

# 3. 원격 저장소로 푸시 (배포 트리거)
git push origin main
```

## ⚠️ Check Point (필수 확인 사항)

1.  **Repository Settings 변경:**
    - GitHub Repo -> `Settings` -> `Pages` -> Build and deployment -> Source 항목을 **`GitHub Actions`**로 변경했는가? (가장 중요)
2.  **Next.js Config 확인:**
    - `output: "export"` 설정이 빠지면 빌드 후 `out` 폴더가 생성되지 않아 배포가 실패함.
    - `images.unoptimized: true` 설정이 빠지면 `<Image />` 컴포넌트 사용 시 빌드 에러 발생함.
3.  **패키지 의존성:**
    - `package-lock.json`이 깃에 올라가 있어야 `npm ci` 명령어가 정상 작동함.
