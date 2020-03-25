<template>
  <div>
      <div v-if="!received">
          <div v-if="!selectedFile">
              <h2>Select an Image</h2>
              <input type="file" accept="image/jpeg" name="image" @change="uploadImage">
          </div>
          <div v-else>
              <h2>{{ title }}</h2>
              <img :src="selectedFile" class="sample">
              <button @click="removeImage">Remove</button>
          </div>
            <br>
            <br>
            <button @click="onSubmit">Send</button>
      </div>
      <div v-else>
        <div v-if="!mergedImage">
              <div id="rgbImages">
                  <div>
                    <h2>Red</h2>
                    <img :src="arrImage[0]">
                  </div>
                  <div>
                    <h2>Green</h2>
                    <img :src="arrImage[1]">
                  </div>
                  <div>
                    <h2>Blue</h2>
                    <img :src="arrImage[2]">
                  </div>
                </div>
                <br>
              <button @click="onCombine">Combine</button>
          </div>
          <div v-else>
            <h2>Channels Merged</h2>
            <img :src="mergedImage" class="sample">
          </div>
          <br><br>
        <button @click="reset">Go back</button>
      </div>
      <div
          class="vue-ui-loading-indicator"
          aria-hidden="true"
          aria-live="polite"
          aria-label="Loading..."
          role="status"
        >
        <div class="animation" v-if="loading"></div>
      </div>
    </div>
</template>
<script>
import axios from 'axios';

export default {
  name : 'HelloWorld',
  data() {
    return {
      msg : '',
      title:'',
      selectedFile: false,
      image:null,
      received: false,
      arrImage:[],
      loading:false,
      mergedImage:false
    };
  },
  methods: {
    updateSrc(arr) {
      for(var i =0;i<arr.length;i++){
        var img = arr[i].split('\'')[1]
        this.arrImage[i]= 'data:image/jpeg;base64,'+ img ;
      }
    },
    getResponse() {
      const path = 'http://127.0.0.1:5000/response';
      axios.get(path)
        .then((res)=>{
          this.loading=false;
          this.received=true;
          this.msg = res.data['status'];
          if(this.msg.length>1)
            this.updateSrc(this.msg);
          else{
            var img = this.msg[0].split('\'')[1]
            this.mergedImage ='data:image/jpeg;base64,'+img;
          }
        })
        .catch((error)=>{
          console.log(error);
        });
      },
      sendImage(payload) {
        this.loading=true;
        const path = "http://127.0.0.1:5000/sendImage";
        axios.post(path,payload)
          .then(()=>{
            this.getResponse();
          })
          .catch((error)=>{
            console.log(error); 
          })
      },
      getMerge(payload){
        this.loading=true;
        const path = "http://127.0.0.1:5000/merge";
        console.log(payload);
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
        this.title=this.image.name;
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
      reset() {
        this.removeImage();
        this.received=false;
        this.msg='';
        this.arrImage=[];  
        this.mergedImage=false;
      },
      onSubmit(e){
        e.preventDefault();
        const payload = new FormData();
        payload.append('image',this.image,this.image.name)
        this.sendImage(payload);
      },
      onCombine(e){
        e.preventDefault();
        let payload = {
          data: this.arrImage,
          id: "images"
        }
        this.getMerge(payload);
      }
  }

}
</script>

<style>
#app {
  text-align:center;
}
.sample {
  max-width:315px;
  max-height:445px;
}
img {
  width: 70%;
  margin: auto;
  display: block;
  margin-bottom: 10px;
}
#rgbImages {
  display: flex;
  justify-content: center;
}

.vue-ui-loading-indicator > .animation {
  -webkit-animation: rotating 0.7s linear infinite;
  animation: rotating 0.7s linear infinite;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid transparent;
  border-right-color: #2c3e50;
  border-bottom-color: #2c3e50;
  position: fixed;
  bottom: 50px;
  left: 50%;
}
.vue-ui-loading-indicator .animation {
  border-right-color: #42b983;
  border-bottom-color: #42b983;
}
@keyframes rotating {
  0% {
    -webkit-transform: rotate(0);
    transform: rotate(0);
  }
  100% {
    -webkit-transform: rotate(1turn);
    transform: rotate(1turn);
  }
}
/*.vue-ui-loading-indicator[aria-hidden='false'] {
  opacity: 1;
  visibility: visible;
  z-index: 2;
}
.vue-ui-loading-indicator[aria-hidden='true'] {
  opacity: 0;
  visibility: hidden;
}*/
</style>