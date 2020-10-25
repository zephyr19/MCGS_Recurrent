module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    "plugin:vue/essential",
    "eslint:recommended",
    "plugin:prettier/recommended",
    "@vue/typescript/recommended",
    "@vue/prettier",
    "@vue/prettier/@typescript-eslint"
  ],
  parserOptions: {
    ecmaVersion: 2020
  },
  rules: {
    // rules: {
    //   // allow async-await
    //   'generator-star-spacing': 'off',
    //   // allow debugger during development
    //   'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    //   'space-before-function-paren': ["error", "never"],
    //   'indent': 'off',
    //   'vue/script-indent': [
    //     'error',
    //     2,
    //     {
    //       'baseIndent': 1
    //     }
    //   ]
    // }
  }
};
