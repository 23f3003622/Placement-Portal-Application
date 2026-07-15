<template>
    <div class="container mt-4">

        <div class="card shadow">

            <div class="card-header bg-primary text-white">
                <h3>{{ job.title }}</h3>
            </div>

            <div class="card-body">

                <table class="table table-bordered">
                     <tbody>

                    <tr>
                        <th width="30%">Company</th>
                        <td>{{ job.company }}</td>
                    </tr>

                    <tr>
                        <th>Description</th>
                        <td>{{ job.description }}</td>
                    </tr>

                    <tr>
                        <th>Location</th>
                        <td>{{ job.location }}</td>
                    </tr>

                    <tr>
                        <th>Salary (LPA)</th>
                        <td>{{ job.salary }}</td>
                    </tr>

                    <tr>
                        <th>Skills Required</th>
                        <td>{{ job.skills_required }}</td>
                    </tr>

                    <tr>
                        <th>Eligible Branch</th>
                        <td>{{ job.eligibility_branch }}</td>
                    </tr>

                    <tr>
                        <th>Minimum CGPA</th>
                        <td>{{ job.minimum_cgpa }}</td>
                    </tr>

                    <tr>
                        <th>Application Deadline</th>
                        <td>{{ job.application_deadline }}</td>
                    </tr>
                    </tbody>
                </table>

                <div class="mt-4">

                    <button
                        class="btn btn-success me-2"
                        @click="apply"
                        :disabled="applied"
                    >
                        {{ applied ? "Already Applied" : "Apply" }}
                    </button>

                    <button
                        class="btn btn-secondary"
                        @click="$router.back()"
                    >
                        Go Back
                    </button>

                </div>

            </div>

        </div>

    </div>
</template>

<script>
import axios from "axios";

export default {

    data() {

        return {

            job: {},

            applied: false

        };

    },

    async mounted() {

        await this.loadJob();

    },

    methods: {

        async loadJob() {

            try {

                const token = localStorage.getItem("token");

                const response = await axios.get(

                    `http://127.0.0.1:5000/api/student/jobs/${this.$route.params.id}`,

                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }

                );

                this.job = response.data;

            }

            catch (error) {

                console.error(error);

            }

        },

        async apply() {

            try {

                const token = localStorage.getItem("token");

                const response = await axios.post(

                    `http://127.0.0.1:5000/api/student/apply/${this.job.id}`,

                    {},

                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }

                );

                alert(response.data.message);

                this.applied = true;

                this.$router.push("/student");

            }

            catch (error) {

                if (error.response) {

                    alert(error.response.data.message);

                } else {

                    alert(error.message);

                }

            }

        }

    }

}
</script>