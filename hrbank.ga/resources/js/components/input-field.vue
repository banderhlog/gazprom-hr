<template>
  <div class="input-field" :class="fieldClass" @mouseenter="mouseenter" @mouseleave="mouseleave">
    <div class="input-field__placeholder">{{ title }}</div>
    <input type="text" class="input-field__input" @focusin="focusin" @focusout="focusout">
  </div>
</template>

<script>
export default {
  props: ['title'],

  data(){
    return {
      hover: false,
      focus: false,
    };
  },
  methods: {
    mouseenter(){
      this.hover = true;
    },
    mouseleave(){
      this.hover = false;
    },
    focusin(){
      this.focus = true;
    },
    focusout(){
      this.focus = false;
    }
  },
  computed: {
    fieldClass(){
      let fieldClass;
      if (this.focus){
        fieldClass = 'input-field_focus';
      } else if (this.hover){
        fieldClass = 'input-field_hover';
      }
      return fieldClass;
    }
  },
  mounted() {

  }
}
</script>