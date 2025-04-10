<template>
<div class="complaint-main">
  <h1>고소장 초안</h1>
  <table class="complaint-table">
    <tbody>
      <tr><th>고소 취지</th></tr>
      <tr><td>{{ complaint.purpose }} </td></tr>
      <tr><th>고소 이유 </th></tr>
      <tr><td> {{ complaint.reason }} </td></tr>
    </tbody>
  </table>
  <div class="line-divider">
    이하는 의뢰인과 유사한 상황이었던 분들이 재판을 진행했던 결과입니다.
  </div>
    <v-row class="cases" dense>
      <v-col
        v-for="(f, i) in facts"
        :key="i"
        cols="12"
        md="4"
      >
      <v-card
        variant="outlined"
        class="mx-auto"
        max-width="344"
        @click="popDialog(i)"
        link
      >
      <v-card-title>{{ '유사 판례 '+(i+1) }}</v-card-title>
      <v-card-text> 
        <h4>사건</h4>
        <div class="one-line">{{ f.facts }}</div>
        <h4>판결</h4>
        <div class="one-line">{{ f.ruling }}</div>
      </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</div>
<v-dialog
  v-model="dialog"
  width="auto"
  class="case-dialog"
>
  <v-card max-width="600">
    <v-card-title>{{ dialogTitle }}</v-card-title>
    <v-card-text>
      <h3>사건</h3>
      <div class="dialog-body">{{ dialogSubtitle }}</div>
      <h3>판결</h3>
      <div class="dialog-body">{{  dialogText }}</div>
    </v-card-text>
    <template v-slot:actions>
      <v-btn
        class="ms-auto"
        text="Close"
        @click="dialog = false"
      ></v-btn>
    </template>
  </v-card>
</v-dialog>
</template>
<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "Complaint",
  props: [ "info", "complaint", "facts" ],
  data() {
    return {
        dialogTitle: '',
        dialogText: '',
        dialogSubtitle: '',
        dialog: false,
    }
  },
  methods: {
    popDialog(i) {
      if (this.facts.length == 0) {
        return;
      }
      this.dialogTitle = "유사 판례 " + (i+1)
      this.dialogSubtitle = this.facts[i].facts
      this.dialogText = this.facts[i].ruling
      this.dialog = true
    }
  }
});
</script>
<style>
.cases {
  padding:40px 20px 0 20px;
  color: #333;
}
/* .case .v-card-title {
  font-weight: bolder  ;
} */
.cases .one-line {
  color: #555;
  white-space: nowrap;
  padding-bottom: 7px;
  font-size: 12px;
  text-overflow: ellipsis;
  overflow: hidden; 
}
.cases .v-card-title {
  font-size: 15px !important;
}
.cases .v-card-subtitle {
  font-size: 11px !important;
}
/* .case-dialog .v-card-title {
} */
.line-divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: #999;
  padding-top: 40px;
}
.line-divider::before,
.line-divider::after {
  width: 200px;
  content: "";
  flex: 1;
  border-bottom: 1px solid #aaa;
  margin: 0 16px;
}
th {
  padding: 5px;
  border: 1px solid black;
  line-height: 20px;
  /* font-size: 18px; */
  text-align: center;
}
td {
    padding: 5px 10px;
    border: 1px solid black;
    line-height: 23px;
}
.complaint-table {
    width: 100%;
    border-collapse: collapse;
    border: 2px solid black;
}
.complaint-main {
  padding: 20px 70px 0 70px;
}
table {
  font-size: 14px;
}
h1 {
  text-align: center;
  line-height: 50px;
  font-size: 25px;
}
h3 {
  line-height: 30px;
  font-size: 17px;
  font-weight: 600;
}
.dialog-body {
  font-size:15px;
  margin: 6px 0;
  line-height: 20px;
}
</style>