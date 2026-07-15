<template>
<div class="container mt-4">

    <!-- Header -->
    <div class="card shadow mb-4">
        <div class="card-header bg-primary text-white text-center py-3">
            <h2 class="mb-1">Next Step</h2>
            <p class="mb-0">Student Application History</p>
        </div>
    </div>

    <!-- Student Details -->
    <div class="card mb-4">
        <div class="card-body d-flex justify-content-between align-items-center">

            <div>
                <h5 class="text-primary mb-2">
                    {{ student.name }}
                </h5>

                <p class="mb-0">
                    <strong>Department:</strong>
                    {{ student.branch }}
                </p>
            </div>

            <div>

                <button
                    class="btn btn-success me-2"
                    @click="exportApplications"
                >
                    Export Applications
                </button>

                <button
                    class="btn btn-outline-primary"
                    @click="$router.back()"
                >
                    Back
                </button>

            </div>

        </div>
    </div>

    <!-- Application History -->
    <div class="card">

        <div class="card-header bg-primary text-white">
            Application History
        </div>

        <div class="card-body">

            <table class="table table-bordered table-hover mb-0">

                <thead class="table-light">

                    <tr>
                        <th>Drive No.</th>
                        <th>Interview</th>
                        <th>Job Title</th>
                        <th>Company</th>
                        <th>Status</th>
                        <th>Remarks</th>
                    </tr>

                </thead>

                <tbody>

                    <tr
                        v-for="item in history"
                        :key="item.application_id"
                    >

                        <td>{{ item.drive }}</td>

                        <td>{{ item.interview }}</td>

                        <td>{{ item.job_title }}</td>

                        <td>{{ item.company }}</td>

                        <td>

                            <span
                                class="badge"
                                :class="{
                                    'bg-warning': item.result == 'Applied',
                                    'bg-primary': item.result == 'Shortlisted',
                                    'bg-success': item.result == 'Selected',
                                    'bg-danger': item.result == 'Rejected',
                                    'bg-secondary': item.result == 'Waitlisted'
                                }"
                            >
                                {{ item.result }}
                            </span>

                        </td>

                        <td>
                            {{ item.remarks || "None" }}
                        </td>

                    </tr>

                    <tr v-if="history.length === 0">

                        <td colspan="6" class="text-center">
                            No Applications Yet
                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

    </div>

</div>
</template>

<script>

import axios from "axios";

export default{

    data(){

        return{

            student:{},

            history:[]

        }

    },

    async mounted(){

        await this.loadHistory();

    },

    methods:{


        async loadHistory(){

            try{

                const token = localStorage.getItem("token");

                const response = await axios.get(

                    "http://127.0.0.1:5000/api/student/history",

                    {

                        headers:{

                            Authorization:`Bearer ${token}`

                        }

                    }

                );

                this.student = response.data.student;

                this.history = response.data.history;

            }

            catch(error){

                console.log(error);

            }

        },
        async exportApplications(){

    try{

        const token = localStorage.getItem("token");

        const response = await axios.post(

            "http://127.0.0.1:5000/api/export-applications",

            {},

            {

                headers:{
                    Authorization:`Bearer ${token}`
                }

            }

        );

        alert(response.data.message);

    }

    catch(error){

        console.log(error);

        alert("Unable to start export.");

    }

}

    }

}

</script>