import 'animate.css/animate.min.css'
import 'font-awesome/css/font-awesome.min.css'
import './assets/bar.css'
import './assets/buttongroup.css'
import './assets/commafield.css'
import './assets/modals.css'
import './assets/progress.css'
import './assets/shepherd-custom.css'
import './assets/style.css'
import './assets/welcome.css'


// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
