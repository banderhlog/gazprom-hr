<template>
  <div class="list">
    <div v-for="i in 10" class="list__item">
      <svg class="list__item-edit" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill-rule="nonzero" d="M20.185 5.332a1.075 1.075 0 0 1 0 1.52l-1.54 1.54-3.037-3.038 1.541-1.54a1.074 1.074 0 0 1 1.518 0l1.518 1.518zm-5.637 1.083l3.037 3.036-8.61 8.61-3.59 1.393a.65.65 0 0 1-.84-.84l1.394-3.59 8.609-8.609z"></path></svg>
      <div class="list__item-title">middle PHP Developer</div>
      <div class="list__item-text">middle PHP Developer</div>
      <div class="list__item-footer">
        <div class="list__item-footer-left">middle PHP Developer</div>
        <div class="list__item-footer-right">middle PHP Developer</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "tabs",
  props: ['items'],
  data: function () {
    return {
      tabs: JSON.parse(this.items),
      active_id: 0
    }
  },
  methods: {
    active(id) {
      return this.active_id === id ? 'tabs__item_active' : '';
    },
    select(id) {
      this.active_id = id;
    }
  },
  mounted() {

  }
}
</script>