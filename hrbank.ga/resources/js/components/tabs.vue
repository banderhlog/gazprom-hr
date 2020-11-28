<template>
  <div class="tabs">
    <div class="tabs__line"></div>
    <div class="tabs__item" @click="select(0)" :class="active(0)">Все</div>
    <div v-for="tab in tabs" class="tabs__item" @click="select(tab.id)" :class="active(tab.id)">{{ tab.title }}</div>
  </div>
</template>

<script>
export default {
  name: "tabs",
  props: ['items'],
  data: function (){
    return {
      tabs: JSON.parse(this.items),
      active_id: 0
    }
  },
  methods: {
    active(id){
      return this.active_id === id? 'tabs__item_active':'';
    },
    select(id){
      this.active_id = id;
    }
  },
  mounted() {

  }
}
</script>