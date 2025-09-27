# V-Lawyer Documentation

Official documentation for V-Lawyer Platform - AI-powered legal intelligence for developers.

## 🚀 Deployment to Vercel

This documentation site is deployed to [https://docs.v-lawyer.ai](https://docs.v-lawyer.ai)

### Step 1: Push to GitHub

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: V-Lawyer documentation"
git remote add origin https://github.com/v-lawyer/v-lawyer-docs.git
git push -u origin main
```

### Step 2: Deploy with Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New Project"
3. Import the `v-lawyer/v-lawyer-docs` repository
4. Configure build settings:
   - **Framework Preset**: `Other`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`
5. Click "Deploy"

### Step 3: Configure Custom Domain

1. In Vercel project settings, go to "Domains"
2. Add custom domain: `docs.v-lawyer.ai`
3. Configure DNS:
   - Add CNAME record pointing to `cname.vercel-dns.com`
   - Or use A records pointing to Vercel's IP addresses
4. Wait for SSL certificate provisioning (automatic)

## 📁 Project Structure

```
v-lawyer-docs/
├── docs/                  # Documentation content
│   ├── intro.md          # Getting started guide
│   ├── cli/              # Kanuni CLI documentation
│   │   ├── installation.md
│   │   ├── authentication/
│   │   └── commands/
│   ├── api/              # V-Lawyer API documentation
│   │   ├── authentication/
│   │   ├── endpoints/
│   │   └── webhooks.md
│   └── guides/           # User guides and tutorials
├── src/                  # React components
│   ├── components/       # Custom components
│   ├── pages/           # Custom pages
│   └── css/             # Styling
├── static/              # Static assets
│   └── img/            # Images and logos
├── docusaurus.config.ts # Site configuration
├── sidebars.ts         # Sidebar navigation
└── vercel.json         # Vercel configuration
```

## 🛠️ Local Development

```bash
# Install dependencies
npm install

# Start development server (port 3000)
npm start

# Build for production
npm run build

# Test production build locally
npm run serve
```

## 📝 Writing Documentation

### Adding New Pages

1. Create a markdown file in the appropriate `docs/` subdirectory
2. Add frontmatter for metadata:

```markdown
---
sidebar_position: 1
title: Your Page Title
description: Brief description for SEO
---

# Your Content
```

### Syntax Highlighting

The site supports syntax highlighting for:
- Bash/Shell
- Rust
- TypeScript/JavaScript
- JSON
- TOML

Example:
````markdown
```rust
fn main() {
    println!("Hello, V-Lawyer!");
}
```
````

### Adding Images

Place images in `static/img/` and reference them:

```markdown
![Alt text](/img/your-image.png)
```

## 🎨 Customization

- **Colors & Theme**: Edit `src/css/custom.css`
- **Site Config**: Update `docusaurus.config.ts`
- **Navigation**: Modify `sidebars.ts`
- **Homepage**: Edit `src/pages/index.tsx` and `src/components/HomepageFeatures/`

## 📚 Documentation Coverage

### Kanuni CLI
- ✅ Installation guide
- ✅ Authentication (OAuth Device Flow & API Keys)
- ✅ Command reference
- ✅ Configuration options
- ⬜ Advanced usage examples

### V-Lawyer API
- ⬜ Authentication overview
- ⬜ REST API endpoints
- ⬜ WebSocket real-time updates
- ⬜ Webhook integration
- ⬜ Rate limiting
- ⬜ Error handling

### Guides
- ⬜ Quick start tutorial
- ⬜ Document analysis workflow
- ⬜ Case law search integration
- ⬜ Building custom integrations
- ⬜ Security best practices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

The documentation is licensed under MIT License.

## 🔗 Links

- **V-Lawyer Platform**: [v-lawyer.ai](https://v-lawyer.ai)
- **Kanuni CLI**: [github.com/v-lawyer/kanuni-cli](https://github.com/v-lawyer/kanuni-cli)
- **API Status**: [status.v-lawyer.ai](https://status.v-lawyer.ai)
- **Support**: [support@v-lawyer.ai](mailto:support@v-lawyer.ai)