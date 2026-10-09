import sonarjs from 'eslint-plugin-sonarjs';

export default [{
  files: ['assets/*.js'],
  languageOptions: {
    ecmaVersion: 2022,
    sourceType: 'script',
    globals: Object.fromEntries(['document', 'window', 'location', 'navigator',
      'URL', 'URLSearchParams', 'setTimeout', 'CV_REFERENCES'].map(name => [name, 'readonly'])),
  },
  plugins: { sonarjs },
  rules: {
    'complexity': ['error', 6],
    'sonarjs/cognitive-complexity': ['error', 10],
    'no-undef': 'error',
    'no-unreachable': 'error',
  },
}];
