<template>

<div class="container mt-4">

    <button
        class="btn btn-secondary mb-3"
        @click="$router.back()"
    >
        Back
    </button>

    <div class="card shadow">

        <div class="card-header bg-primary text-white">
            <h3>Student Details</h3>
        </div>

        <div class="card-body">

            <p><strong>Name :</strong> {{ student.name }}</p>

            <p><strong>Branch :</strong> {{ student.branch }}</p>

            <p><strong>Year :</strong> {{ student.year }}</p>

            <p><strong>CGPA :</strong> {{ student.cgpa }}</p>

            <p><strong>Phone :</strong> {{ student.phone }}</p>

            <p><strong>Placement :</strong> {{ student.placement_status }}</p>

            <p><strong>Skills :</strong></p>

            <p>{{ student.skills || "Not Added" }}</p>

            <p><strong>Experience :</strong></p>

            <p>{{ student.experience || "None" }}</p>

            <p>

                <strong>Resume :</strong>

                <a
                    v-if="student.resume"
                    :href="student.resume"
                    target="_blank"
                >
                    View Resume
                </a>

                <span v-else>
                    Not Uploaded
                </span>

            </p>

        </div>

    </div>

    <div class="card shadow mt-4">

        <div class="card-header bg-primary text-white">

            <h4>Application History</h4>

        </div>

        <table class="table table-bordered mb-0">

            <thead>

                <tr>

                    <th>Company</th>

                    <th>Job Title</th>

                    <th>Status</th>

                    <th>Applied Date</th>

                    <th>Remarks</th>

                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="app in applications"
                    :key="app.application_id"
                >

                    <td>{{ app.company }}</td>

                    <td>{{ app.job_title }}</td>

                    <td>

                        <span
                            class="badge"
                            :class="{

                                'bg-warning': app.status=='Applied',

                                'bg-primary': app.status=='Shortlisted',

                                'bg-success': app.status=='Selected',

                                'bg-danger': app.status=='Rejected',

                                'bg-secondary': app.status=='Waitlisted'

                            }"
                        >

                            {{ app.status }}

                        </span>

                    </td>

                    <td>{{ app.applied_at }}</td>

                    <td>{{ app.remarks || "None" }}</td>

                </tr>

                <tr v-if="applications.length==0">

                    <td
                        colspan="5"
                        class="text-center"
                    >

                        No Applications Found

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

            student:{},

            applications:[]

        }

    },

    async mounted(){

        this.loadStudent();

    },

    methods:{

        async loadStudent(){

            try{

                const token = localStorage.getItem("token");

                const response = await axios.get(

                    `http://127.0.0.1:5000/api/admin/student/${this.$route.params.id}`,

                    {

                        headers:{

                            Authorization:`Bearer ${token}`

                        }

                    }

                );

                this.student = response.data.student;

                this.applications = response.data.applications;

            }

            catch(error){

                console.log(error);

            }

        }

    }

}

</script>