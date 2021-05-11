import Vue from 'vue'
import Vuex from 'vuex'

import tagsView from './modules/tagsView'
import getters from './getters'


Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    tagsView,
  },
  getters
})

export default store
