import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { siteOrigin, siteBase, documentationRepository } from './site.config.mjs';
import { martianCodeBlocks } from './src/lib/code-blocks.mjs';

export default defineConfig({
  site: siteOrigin,
  base: siteBase,
  trailingSlash: 'always',
  integrations: [starlight({
    title: 'Martian Security',
    description: 'Customer guides for red teaming, Evals, the SDK and CI.',
    favicon: '/favicon.png',
    components: {
      SiteTitle: './src/components/SiteTitle.astro',
      PageTitle: './src/components/PageTitle.astro',
      ThemeProvider: './src/components/ThemeProvider.astro',
    },
    social: [{ icon: 'github', label: 'GitHub', href: documentationRepository }],
    editLink: { baseUrl: `${documentationRepository}/edit/main/` },
    customCss: ['./src/styles/custom.css'],
    expressiveCode: {
      themes: ['github-dark', 'github-light'],
      plugins: [martianCodeBlocks],
      defaultProps: { wrap: false, frame: 'code' },
      frames: {
        showCopyToClipboardButton: true,
        extractFileNameFromCode: false,
        removeCommentsWhenCopyingTerminalFrames: false,
      },
      styleOverrides: {
        borderRadius: '10px',
        borderColor: 'var(--sl-color-hairline)',
        codeFontFamily: 'var(--sl-font-mono)',
        uiFontFamily: 'Inter Variable, Inter, sans-serif',
        codeFontSize: '0.8125rem',
        codeLineHeight: '1.75',
        codePaddingBlock: '1rem',
        codeBackground: 'var(--code-block-bg)',
        frames: {
          shadowColor: 'transparent',
          editorBackground: 'var(--code-block-bg)',
          editorTabBarBackground: 'var(--code-block-header)',
          editorTabBarBorderBottomColor: 'var(--sl-color-hairline)',
          editorActiveTabBackground: 'transparent',
          editorActiveTabForeground: 'var(--sl-color-gray-2)',
          editorActiveTabIndicatorHeight: '0px',
          terminalBackground: 'var(--code-block-bg)',
          terminalTitlebarDotsOpacity: '0',
          terminalTitlebarBackground: 'var(--code-block-header)',
          terminalTitlebarForeground: 'var(--sl-color-gray-2)',
        },
      },
    },
    sidebar: [
  {
    "label": "Overview",
    "slug": ""
  },
  {
    "label": "Get started",
    "items": [
      {
        "autogenerate": {
          "directory": "get-started"
        }
      }
    ]
  },
  {
    "label": "Agents and environments",
    "collapsed": true,
    "items": [
      {
        "autogenerate": {
          "directory": "agents"
        }
      },
      {
        "autogenerate": {
          "directory": "environments"
        }
      }
    ]
  },
  {
    "label": "Red teaming",
    "collapsed": true,
    "items": [
      {
        "autogenerate": {
          "directory": "assessments"
        }
      }
    ]
  },
  {
    "label": "Evals",
    "collapsed": true,
    "items": [
      {
        "autogenerate": {
          "directory": "evals"
        }
      }
    ]
  },
  {
    "label": "Scanner",
    "collapsed": true,
    "items": [
      {
        "autogenerate": {
          "directory": "scanner"
        }
      }
    ]
  },
  {
    "label": "SDK and CI",
    "collapsed": true,
    "items": [
      {
        "autogenerate": {
          "directory": "sdk"
        }
      }
    ]
  },
  {
    "label": "Move from another tool",
    "collapsed": true,
    "items": [
      {
        "autogenerate": {
          "directory": "migrate"
        }
      }
    ]
  },
  {
    "label": "Discovery",
    "collapsed": true,
    "items": [
      {
        "autogenerate": {
          "directory": "discovery"
        }
      }
    ]
  },
  {
    "label": "Attack library",
    "collapsed": true,
    "items": [
      { "label": "Attack reference", "slug": "library/attacks" },
      { "label": "Use the library and coverage views", "slug": "library/coverage" },
      {
        "label": "Attack families",
        "collapsed": true,
        "items": [{ "autogenerate": { "directory": "attacks" } }]
      },
      {
        "label": "Security frameworks",
        "collapsed": true,
        "items": [{ "autogenerate": { "directory": "frameworks" } }]
      }
    ]
  },
  {
    "label": "Workspace",
    "collapsed": true,
    "items": [
      { "autogenerate": { "directory": "workspace" } }
    ]
  },
  {
    "label": "Reference",
    "collapsed": true,
    "items": [
      {
        "autogenerate": {
          "directory": "reference"
        }
      }
    ]
  },
  {
    "label": "Hermes documentation \u2197",
    "link": "https://martiansecurity.github.io/martian-hermes-docs/"
  }
],
  })],
});
