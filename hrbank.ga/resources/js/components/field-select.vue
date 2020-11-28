<template>
  <div class="input-field" :class="fieldClass" @mouseenter="mouseenter" @mouseleave="mouseleave">
    <div class="input-field__placeholder" :class="placeholderClass">{{ title }}</div>
    <input v-model="value" type="text" class="input-field__input" @focusin="focusin" @focusout="focusout">
    <div class="input-field__select" :class="selectClass">
      <div @click="select(item.id, i)" v-for="(item, i) in items" class="input-field__option">{{ item.title }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['title', 'options', 'multiple'],
  data() {
    return {
      hover: false,
      focus: false,
      value: '',
      items: typeof this.options === "string" ? JSON.parse(this.options) : this.options,
      selected: false,
      selected_index: false,
      multiple_selected: []
    };
  },
  methods: {
    mouseenter() {
      this.hover = true;
    },
    mouseleave() {
      this.hover = false;
    },
    focusin() {
      this.focus = true;
    },
    focusout() {
      setTimeout(() => {
        this.focus = false;
      }, 200);
    },
    select(id, index) {
      if (this.multiple){
        this.multiple_selected.push(index);
      } else {
        this.selected_id = id;
        this.selected_index = index;
        this.value = this.items[index].title;
        this.$emit('input', this.items[index]);
      }
    }
  },
  computed: {
    fieldClass() {
      let result;
      if (this.focus) {
        result = 'input-field_focus';
      } else if (this.hover) {
        result = 'input-field_hover';
      }

      return result;
    },
    placeholderClass() {
      let result;
      if (this.value.length > 0) {
        result = 'input-field__placeholder_pined'
      }

      if (this.focus) {
        result = 'input-field__placeholder_focus input-field__placeholder_pined';
      }

      return result;
    },
    selectClass() {
      return this.focus ? 'input-field__select_active' : '';
    }
  },
  mounted() {

  }
}
</script>