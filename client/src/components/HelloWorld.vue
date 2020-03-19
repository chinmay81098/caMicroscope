<template>
  <div>
  <div v-if="!selectedFile">
    <h2>Select an Image</h2>
    <input type="file" accept="image/jpeg" name="image" @change="uploadImage">
  </div>
  <div v-else>
    <img :src="selectedFile">
    <button @click="removeImage">Remove</button>
  </div>
  <button @click="onSubmit">Send</button>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  name : 'HelloWorld',
  data() {
    return {
      msg : '',
      selectedFile: false,
      image:null,
    };
  },
  methods: {
    getResponse() {
      const path = 'http://127.0.0.1:5000/response';
      axios.get(path)
        .then((res)=>{
          this.msg = res.data;
        })
        .catch((error)=>{
          console.log(error);
        });
      },
      sendImage(payload) {
        const path = "http://127.0.0.1:5000/upload-image";
        axios.post(path,payload)
          .then(()=>{
            this.getResponse();
          })
          .catch((error)=>{
            console.log(error);
          })
      },
      uploadImage(event){
        var file = event.target.files[0];
        this.image=file;
        this.createImage(file);
      },
      createImage(file) {
        //var image = new Image();
        var reader = new FileReader();

        reader.onload=(e)=>{
          this.selectedFile = e.target.result;
          };
        reader.readAsDataURL(file);
      },
      removeImage() {
        this.selectedFile=false;
      },
      onSubmit(e){
        e.preventDefault();
        const payload = new FormData();
        payload.append('image',this.image,this.image.name);
        this.sendImage(payload);
      },

  }

}
</script>

<style>
#app {
  text-align:center;
}
img {
  width: 30%;
  margin: auto;
  display: block;
  margin-bottom: 10px;
}
</style>