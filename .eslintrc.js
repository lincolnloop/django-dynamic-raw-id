module.exports = {
  "env": {
    "browser": true,
    "commonjs": true,
    "es6": true
  },
  "parserOptions": {
    "ecmaFeatures": {
      "experimentalObjectRestSpread": true
    },
    "sourceType": "module"
  },
  "globals" : {
    "window": true
  },
  "extends": ["eslint:recommended"],
  "rules": {
    "indent": [
      "error",
      2
    ],
    "linebreak-style": [
      1,
      "unix"
    ],
    "quotes": [
      1,
      "single"
    ],
    "semi": [
      1,
      "always"
    ],
    "eol-last": "error",
    "comma-spacing": ["error", {"before": false, "after": true}],
    "space-before-function-paren": ["error", "never"],
    "space-in-parens": ["error", "never"],
    "keyword-spacing": [
      "error", {
        "before": true,
        "after": true,
        "overrides": {
          "throw": {
            "after": false
          }
        }
      }
    ]
  }
};
