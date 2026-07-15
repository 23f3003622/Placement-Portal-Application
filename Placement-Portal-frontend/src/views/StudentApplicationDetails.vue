<template>

<div class="container mt-4">

    <div class="d-flex justify-content-between mb-4">

        <h2>Application Details</h2>

        <button
            class="btn btn-secondary"
            @click="$router.back()"
        >
            Back
        </button>

    </div>

    <div class="card p-4">

        <h4>{{ application.job.title }}</h4>

        <p>
            <strong>Company:</strong>
            {{ application.company.company_name }}
        </p>

        <p>
            <strong>Status:</strong>

            <span class="badge bg-primary">
                {{ application.status }}
            </span>
        </p>

        <hr>

        <h5>Job Description</h5>

        <p>{{ application.job.description }}</p>

        <p>

            <strong>Location:</strong>

            {{ application.job.location }}

        </p>

        <p>

            <strong>Salary:</strong>

            {{ application.job.salary }} LPA

        </p>

        <p>

            <strong>Skills Required:</strong>

            {{ application.job.skills_required }}

        </p>

        <hr>

        <h5>Company Remarks</h5>

        <p>

            {{ application.remarks || "No remarks yet." }}

        </p>

        <div
            v-if="application.status=='Shortlisted'"
            class="mt-4"
        >

            <div class="alert alert-success">

                <h5>Interview Scheduled</h5>

                <hr>

                <p>

                    <strong>Interview Type:</strong>

                    {{ application.interview.type }}

                </p>

                <p>

                    <strong>Date:</strong>

                    {{ application.interview.date }}

                </p>

                <p>

                    <strong>Time:</strong>

                    {{ application.interview.time }}

                </p>

                <div
                    v-if="application.interview.type=='Online'"
                >

                    <strong>Meeting Link:</strong>

                    <a
                        :href="application.interview.link"
                        target="_blank"
                    >
                        Join Interview
                    </a>

                </div>

                <div
                    v-else
                >

                    <strong>Location:</strong>

                    {{ application.interview.location }}

                </div>

            </div>

        </div>

    </div>

</div>

</template>

<script>

import axios from "axios";

export default{

data(){

return{

application:{

job:{},

company:{},

interview:{}

}

}

},

async mounted(){

this.loadApplication();

},

methods:{

async loadApplication(){

const token=localStorage.getItem("token");

const response=await axios.get(

`http://127.0.0.1:5000/api/student/applications/${this.$route.params.id}`,

{

headers:{

Authorization:`Bearer ${token}`

}

}

);

this.application=response.data;

}

}

}

</script>