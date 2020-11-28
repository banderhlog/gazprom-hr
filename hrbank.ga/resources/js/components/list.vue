<template>
  <div class="list">
    <div class="list__item card"></div>
    <div class="list__item card"></div>
    <div class="list__item card"></div>
    <div class="list__item card"></div>
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