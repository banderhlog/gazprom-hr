<template>
  <div class="req">
    <div class="" v-if="lines.length">
      <div v-for="(line, i) in lines" class="input-field__wrapper row">
        <div class="col-6">
          <field-select v-model="lines[i].selected_requirement" title="Характеристика" :options="req"></field-select>
        </div>
        <div class="col-6" v-if="checkSelectYear(line)">
          <field-select title="Опыт работы" :options="[{id: 1, title: '1'}, {id: 2, title: '2'}]"></field-select>
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
  data: function (){
    return {
      requirements: JSON.parse(this.req),
      lines: []
    }
  },
  methods: {
    addLine(){
      this.lines.push({
       selected_requirement: null
      })
    },
    checkSelectYear(line){
      if (line.selected_requirement){
        if (line.selected_requirement.type === 'select-years'){
          return true;
        }
      }
      return false;
    }
  }
}
</script>