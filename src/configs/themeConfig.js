// You can customize the template with the help of this file
// ================================================================================================
//  File Name: themeConfig.js
//  Description: Details Pages of the Config ( Theme Config settings ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
//Template config options
const themeConfig = {
  app: {
    appName: 'XDR Master',
    appLogoImage: require('@src/assets/images/logo/logo.png').default
  },
  layout: {
    isRTL: false,
    skin: 'light', // light, dark, bordered, semi-dark
    routerTransition: 'fadeIn', // fadeIn, fadeInLeft, zoomIn, none or check this for more transition https://animate.style/
    type: 'vertical', // vertical, horizontal
    contentWidth: 'full', // full, boxed
    menu: {
      isHidden: false,
      isCollapsed: false
    },
    navbar: {
      // ? For horizontal menu, navbar type will work for navMenu type
      type: 'floating', // static , sticky , floating, hidden
      backgroundColor: 'white' // BS color options [primary, success, etc]
    },
    footer: {
      type: 'static' // static, sticky, hidden
    },
    customizer: true,
    scrollTop: true // Enable scroll to top button
  }
}

export default themeConfig
