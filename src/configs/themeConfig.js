// =============================================================================================
//  File Name: themeConfig.js
//  Description: Details of the customize the template component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// You can customize the template with the help of this file

//Template config options
const themeConfig = {
  app: {
    appName: 'SRC',
    appLogoImage: require('@src/assets/images/logo/logo3.png').default
  },
  layout: {
    isRTL: false,
    skin: 'dark', // light, dark, bordered, semi-dark
    routerTransition: 'zoomIn', // fadeIn, fadeInLeft, zoomIn, none or check this for more transition https://animate.style/
    type: 'vertical', // vertical, horizontal
    contentWidth: 'full', // full, boxed
    menu: {
      isHidden: false,
      isCollapsed: true
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
