<template>
  <div class="req">
    <div class="" v-if="lines.length">
      <div v-for="(line, i) in lines" class="input-field__wrapper row">
        <div class="col-6">
          <field-select v-model="lines[i].selected_requirement" title="Характеристика" :options="req"></field-select>
        </div>
        <div class="col-6" v-if="line.selected_requirement">
          <field-select v-if="checkSelectYear(line)" title="Опыт работы" :options="years"></field-select>
          <!--          <field-select v-if="checkSelectOptions(line)" multiple="true" title="asdasd" :options="line.selected_requirement.options"></field-select>-->
          <multiselect v-if="checkSelectOptions(line)" v-model="line.options" :multiple="true" placeholder="Дополнительно"
                       label="title" :options="getSelectedOptions(line.selected_requirement.options)"></multiselect>
        </div>
      </div>
    </div>
    <button @click="addLine" class="btn btn_sm btn_blue">Добавить</button>
  </div>
</template>

<script>
export default {
  name: "requirements",
  props: ['req'],
  data: function () {
    return {
      requirements: JSON.parse(this.req),
      lines: [],
      years: [
        {id: 1, title: 'Без опыта'},
        {id: 2, title: 'От 1 года до 3 лет'},
        {id: 3, title: 'От 3 до 6 лет'},
        {id: 4, title: 'Более 6 лет'}
      ]
    }
  },
  methods: {
    addLine() {
      this.lines.push({
        selected_requirement: null,
        options: []
      })
    },
    checkSelectYear(line) {
      return line.selected_requirement.type === 'select-years';
    },
    checkSelectOptions(line) {
      return line.selected_requirement.type === 'select-options';
    },
    getSelectedOptions(options) {
      return options.map(option => {
        if (option.type === 'version') {
          option.title = option.title.includes('v') ? option.title : 'v' + option.title;
        }
        return option;
      })
    }
  }
}
</script>