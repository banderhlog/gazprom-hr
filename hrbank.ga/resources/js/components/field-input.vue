<template>
  <div class="input-field__wrapper">
    <div class="input-field" :class="fieldClass" @mouseenter="mouseenter" @mouseleave="mouseleave">
      <div class="input-field__placeholder" :class="placeholderClass">{{ title }}</div>
      <input v-model="value" :type="type" :name="name" class="input-field__input" @focusin="focusin" @focusout="focusout">
    </div>
    <div v-if="error" class="input-field__error">{{ error }}</div>
  </div>
</template>

<script>
export default {
  props: ['title', 'error', 'type', 'name'],

  data(){
    return {
      hover: false,
      focus: false,
      value: ''
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
      let result;
      if (this.focus){
        result = 'input-field_focus';
      } else if (this.hover){
        result = 'input-field_hover';
      }

      return result;
    },
    placeholderClass(){
      let result;
      if (this.value.length > 0){
        result = 'input-field__placeholder_pined'
      }

      if (this.focus){
        result = 'input-field__placeholder_focus input-field__placeholder_pined';
      }

      return result;
    }
  },
  mounted() {

  }
}
</script>