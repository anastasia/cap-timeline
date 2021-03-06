import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    slug: "",
    title: "",
    subtitle: "",
    groups: {},
    groupsByRegion: [],
    groupNames: {},
    themes: [],
    symbolTranslation: {
      jewish: 'diamond-1',
      indian: 'circle-3',
      chinese: 'circle-2',
      japanese: 'circle-1',
      mexican: 'polygon-2',
      russian: 'diamond-2',
      italian: 'square-2',
    },
    eventTypes: {
      us: false,
      world: false,
      legislation: false,
      caselaw: false,
    },
    eventTranslation: {
      us: "U.S. Event",
      world: "World Event",
      legislation: "Legislation",
      caselaw: "Case Law"
    },
    event: null,
    year: null,
    absoluteMinYear: 1850,
    absoluteMaxYear: 1930,
    minYear: null,
    maxYear: null,
    activateAllGroupsWhenLoaded: false,
    zoomLevel: 1,
  },
  actions: {
    setTimelineSlug(context, slug) {
      context.commit('setTimelineSlug', slug)
    },
    setMetadata(context) {
      let url = process.env.VUE_APP_BACKEND_DATA_URL + context.state.slug + '/meta';
      axios.get(url)
          .then((response) => {
            context.commit('setMetadata', response.data)
          })

    },
    loadGroups(context) {
      let url = process.env.VUE_APP_BACKEND_DATA_URL + context.state.slug + '/groups';
      axios.get(url)
          .then((response) => {
            context.commit('loadGroups', response.data)
          })
    },
    loadGroupsByRegion(context) {
      let url = process.env.VUE_APP_BACKEND_DATA_URL + context.state.slug + '/groups-by-region';
      axios.get(url)
          .then((response) => {
            context.commit('loadGroupsByRegion', response.data)
          })
    },
    loadYears(context) {
      let url = process.env.VUE_APP_BACKEND_DATA_URL + context.state.slug + '/year-settings';
      axios.get(url)
          .then((response) => {
            context.commit('loadYears', response.data)
          })
    },
    loadThemes(context) {
      let url = process.env.VUE_APP_BACKEND_DATA_URL + context.state.slug + '/themes';
      axios.get(url)
          .then((response) => {
            context.commit('loadThemes', response.data)
          })
    },
  },
  mutations: {
    setTimelineSlug(state, slug) {
      state.slug = slug;
      localStorage.setItem('slug', slug)
    },
    setMetadata(state, meta) {
      state.title = meta.title;
      state.subtitle = meta.subtitle;
      localStorage.setItem('title', meta.title);
      localStorage.setItem('subtitle', meta.subtitle);
    },
    loadGroups(state, groups) {
      // work around:
      // we're getting URL parameters before groups are loaded from the server
      // because of this, we're checking if groups have already been initialized with their correct status
      // otherwise we're hiding groups from view

      state.groups ={};
      for (let i = 0; i < groups.length; i++) {
        if (!(state.groups[groups[i][0]]))
          if (state.activateAllGroupsWhenLoaded) {
            Vue.set(state.groups, groups[i][0], true);
          } else {
            Vue.set(state.groups, groups[i][0], false);
          }
          Vue.set(state.groupNames, groups[i][0], groups[i][1]);
      }
      state.activateAllGroupsWhenLoaded = false;
    },
    loadGroupsByRegion(state, groupsByRegion) {
      state.groupsByRegion = groupsByRegion;
    },
    loadYears(state, years) {
      state.absoluteMinYear = years.min;
      state.absoluteMaxYear = years.max;
    },
    setGroupStatus(state, groupData) {
      if (Object.keys(state.groups).indexOf(groupData.slug) < 0) {
        // state.groups has not been initialized yet, initialize group ourselves
        Vue.set(state.groups, groupData.slug, groupData.status);
      } else {
        state.groups[groupData.slug] = groupData.status;
      }
    },
    setSelectedEvent(state, event) {
      state.event = event;
    },
    setMinYear(state, year) {
      state.minYear = year;
    },
    setMaxYear(state, year) {
      state.maxYear = year;
    },
    setEventStatus(state, eventData) {
      state.eventTypes[eventData.name] = eventData.status;
    },
    activateAllEvents(state) {
      for (let event in state.eventTypes) {
        state.eventTypes[event] = true;
      }
    },
    activateAllGroups(state) {
      // See "work around" note above
      if (Object.keys(state.groups).length === 0)
        state.activateAllGroupsWhenLoaded = true;
      for (let group in state.groups) {
        state.groups[group] = true;
      }
    },
    setZoomLevel(state, zoomLevel) {
      state.zoomLevel = zoomLevel;
    },
    loadThemes(state, themes) {
      state.themes = themes
    }
  },
  getters: {
    getSlug(state) {
      return state.slug;
    },
    getTitle(state) {
      return state.title;
    },
    getGroups(state) {
      return state.groups;
    },
    getActiveGroups(state) {
      // TODO: this is done for every event. Come up with a better soluton.
      return Object.keys(state.groups).filter(group => state.groups[group])
    },
    getGroup: (state) => (slug) => {
      return state.groups[slug]
    },
    getGroupName: (state) => (slug) => {
      return state.groupNames[slug]
    },
    getSelectedEvent(state) {
      return state.event;
    },
    getMinYear(state) {
      return state.minYear
    },
    getMaxYear(state) {
      return state.maxYear
    },
    getSymbolTranslation(state) {
      return state.symbolTranslation
    },
    getEventTypes(state) {
      return state.eventTypes
    },
    getEventTranslation(state) {
      return state.eventTranslation
    },
    getActiveEvents(state) {
      return Object.keys(state.eventTypes).filter(event => state.eventTypes[event])
    },
    getEventStatus: (state) => (name) => {
      return state.eventTypes[name]
    },
    getGroupsByRegion(state) {
      return state.groupsByRegion;
    },
    getAbsoluteMinYear(state) {
      return state.absoluteMinYear;
    },
    getAbsoluteMaxYear(state) {
      return state.absoluteMaxYear;
    },
    getZoomLevel(state) {
      return state.zoomLevel;
    },
    getThemes(state) {
      return state.themes;
    }
  },
});
export default store

