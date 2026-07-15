<template>

<div class="container mt-4">

    <div class="d-flex justify-content-between mb-4">

        <h2>Scheduled Interviews</h2>

        <button
            class="btn btn-secondary"
            @click="$router.back()"
        >
            Back
        </button>

    </div>

    <table class="table table-bordered">

        <thead>

            <tr>

                <th>Sr No.</th>

                <th>Student</th>

                <th>Drive</th>

                <th>Date</th>

                <th>Time</th>

                <th>Type</th>

                <th>Action</th>

            </tr>

        </thead>

        <tbody>

            <tr
                v-for="(interview,index) in interviews"
                :key="interview.id"
            >

                <td>{{ index+1 }}</td>

                <td>{{ interview.student }}</td>

                <td>{{ interview.job }}</td>

                <td>{{ interview.date }}</td>

                <td>{{ interview.time }}</td>

                <td>{{ interview.type }}</td>

                <td>

                    <button
                        class="btn btn-primary btn-sm"
                        @click="viewApplication(interview.id)"
                    >
                        View
                    </button>

                </td>

            </tr>

            <tr v-if="interviews.length===0">

                <td colspan="7" class="text-center">

                    No Interviews Scheduled

                </td>

            </tr>

        </tbody>

    </table>

</div>

</template>

<script>
import axios from "axios";

export default{

data(){

return{

interviews:[]

}

},

async mounted(){

this.loadInterviews();

},

methods:{

async loadInterviews(){

const token=localStorage.getItem("token");

const response=await axios.get(

"http://127.0.0.1:5000/api/company/interviews",

{

headers:{

Authorization:`Bearer ${token}`

}

}

);

this.interviews=response.data;

},

viewApplication(applicationId){

    this.$router.push(`/company/applications/${applicationId}`);

}

}

}

</script>