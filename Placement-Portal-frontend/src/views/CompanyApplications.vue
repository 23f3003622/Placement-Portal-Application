<template>
    <div class="container mt-4">

        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Applications</h2>

            <router-link
                to="/company/dashboard"
                class="btn btn-secondary"
            >
                Back
            </router-link>
        </div>

        <div class="card p-4">

            <h4>{{ job.title || "Applications" }}</h4>

            <table class="table table-bordered mt-4">

                <thead>
                    <tr>
                        <th>Sr No.</th>
                        <th>Name</th>
                        <th>Branch</th>
                        <th>CGPA</th>
                        <th>Status</th>
                        <th width="160">Action</th>
                    </tr>
                </thead>

                <tbody>

                    <tr
                        v-for="(application,index) in applications"
                        :key="application.id"
                    >
                        <td>{{ index + 1 }}</td>

                        <td>{{ application.student?.name }}</td>

                        <td>{{ application.student?.branch }}</td>

                        <td>{{ application.student?.cgpa }}</td>

                        <td>
                            <span class="badge bg-info">
                                {{ application.status }}
                            </span>
                        </td>

                        <td>

                            <button
                                class="btn btn-primary btn-sm"
                                @click="viewApplication(application)"
                            >
                                View Application
                            </button>

                        </td>

                    </tr>

                    <tr v-if="applications.length===0">

                        <td colspan="6" class="text-center">
                            No students have applied yet.
                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

    </div>
</template>

<script>
import axios from "axios";

export default{

data(){

return{

job:{},

applications:[]

}

},

async mounted(){

await this.loadApplications();

},

methods:{

async loadApplications(){

try{

const token=localStorage.getItem("token");

const response=await axios.get(

`http://127.0.0.1:5000/api/company/jobs/${this.$route.params.id}/applications`,

{

headers:{

Authorization:`Bearer ${token}`

}

}

);

console.log("Applications API:",response.data);

this.job=response.data.job || {};

this.applications=response.data.applications || [];

console.table(this.applications);

}catch(error){

console.error(error);

if(error.response){

alert(error.response.data.message);

}else{

alert("Unable to load applications.");

}

}

},

viewApplication(application){

console.log("Selected Application:",application);

console.log("Application ID:",application.id);

if(!application.id){

alert("Application ID is missing.");

return;

}

this.$router.push({

path:`/company/applications/${application.id}`

});

}

}

}

</script>