<template>
    <div class="container mt-4">

        <!-- Header -->
        <div class="card shadow mb-4">
            <div class="card-header bg-primary text-white text-center py-3">
                <h2 class="mb-1">Next Step</h2>
                <p class="mb-0">Student Dashboard</p>
            </div>
        </div>

        <!-- Welcome Card -->
        <div class="card mb-4">
            <div class="card-body d-flex justify-content-between align-items-center">

                <h5 class="text-primary mb-0">
                    Welcome, {{ student.full_name }}
                </h5>

                <div>

                    <button
                        class="btn btn-outline-primary btn-sm me-2"
                        @click="$router.push('/student/profile/edit')"
                    >
                        Edit Profile
                    </button>

                    <button
                        class="btn btn-outline-secondary btn-sm me-2"
                        @click="$router.push('/student/history')"
                    >
                        History
                    </button>

                    <button
                        class="btn btn-outline-danger btn-sm"
                        @click="logout"
                    >
                        Logout
                    </button>

                </div>

            </div>
        </div>

        <!-- Available Placement Drives -->
        <div class="card mb-4">

            <div class="card-header bg-primary text-white">
                Available Placement Drives
            </div>

            <div class="card-body">

                <div class="row mb-3">

                    <div class="col-md-6">

                        <input
                            type="text"
                            class="form-control"
                            placeholder="Search by Company, Position or Skills"
                            v-model="search"
                            @input="searchJobs"
                        >

                    </div>

                </div>

                <table class="table table-bordered">

                    <thead>

                        <tr>

                            <th>Sr No.</th>
                            <th>Company</th>
                            <th>Drive</th>
                            <th>Action</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="(job,index) in jobs"
                            :key="job.id"
                        >

                            <td>{{ index + 1 }}</td>
                            <td>{{ job.company }}</td>
                            <td>{{ job.title }}</td>

                            <td>

                                <button
                                    class="btn btn-primary btn-sm"
                                    @click="viewJob(job.id)"
                                >
                                    View Details
                                </button>

                            </td>

                        </tr>

                        <tr v-if="jobs.length === 0">

                            <td colspan="4" class="text-center">
                                No Drives Available
                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

        <!-- Applied Drives -->
        <div class="card mb-4">

            <div class="card-header bg-primary text-white">
                Applied Drives
            </div>

            <div class="card-body">

                <table class="table table-bordered mb-0">

                    <thead>

                        <tr>

                            <th>Sr No.</th>
                            <th>Drive Name</th>
                            <th>Company</th>
                            <th>Status</th>
                            <th>Action</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="(application,index) in applications"
                            :key="application.id"
                        >

                            <td>{{ index + 1 }}</td>
                            <td>{{ application.job }}</td>
                            <td>{{ application.company }}</td>

                            <td>

                                <span class="badge bg-info">
                                    {{ application.status }}
                                </span>

                            </td>

                            <td>

                                <button
                                    class="btn btn-primary btn-sm"
                                    @click="viewApplication(application.id)"
                                >
                                    View Details
                                </button>

                            </td>

                        </tr>

                        <tr v-if="applications.length === 0">

                            <td colspan="5" class="text-center">
                                No Applications Yet
                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

        <!-- Upcoming Interviews -->
        <div class="card mb-4">

            <div class="card-header bg-primary text-white">
                Upcoming Interviews
            </div>

            <div class="card-body">

                <table class="table table-bordered mb-0">

                    <thead>

                        <tr>

                            <th>Sr No.</th>
                            <th>Company</th>
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

                            <td>{{ index + 1 }}</td>
                            <td>{{ interview.company }}</td>
                            <td>{{ interview.job }}</td>
                            <td>{{ interview.date }}</td>
                            <td>{{ interview.time }}</td>

                            <td>

                                <span
                                    class="badge"
                                    :class="interview.type === 'Online'
                                        ? 'bg-primary'
                                        : 'bg-success'"
                                >
                                    {{ interview.type }}
                                </span>

                            </td>

                            <td>

                                <button
                                    class="btn btn-primary btn-sm"
                                     @click="viewInterview(interview.id)"
                                >
                                    View
                                </button>

                            </td>

                        </tr>

                        <tr v-if="interviews.length === 0">

                            <td colspan="7" class="text-center">
                                No Upcoming Interviews
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

export default {

    data() {

    return {

        student: {},

        jobs: [],

        applications: [],

        interviews: [],

        search: ""

    };

},

    async mounted() {

    await this.loadProfile();

    await this.loadJobs();

    await this.loadApplications();

    await this.loadInterviews();

},

    methods: {

        async loadProfile() {

            try {

                const token = localStorage.getItem("token");

                const response = await axios.get(

                    "http://127.0.0.1:5000/api/student/profile",

                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }

                );

                this.student = response.data;

            }

            catch (error) {

                console.error(error);

            }

        },

        async loadJobs() {

            try {

                const token = localStorage.getItem("token");

                const response = await axios.get(

                    "http://127.0.0.1:5000/api/student/jobs",

                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }

                );

                this.jobs = response.data;

            }

            catch (error) {

                console.error(error);

            }

        },

        async loadApplications() {

            try {

                const token = localStorage.getItem("token");

                const response = await axios.get(

                    "http://127.0.0.1:5000/api/student/applications",

                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }

                );

                this.applications = response.data;

            }

            catch (error) {

                console.error(error);

            }

        },

        async loadInterviews() {

    try {

        const token = localStorage.getItem("token");

        const response = await axios.get(

            "http://127.0.0.1:5000/api/student/interviews",

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        );

        this.interviews = response.data;

    }

    catch (error) {

        console.error(error);

    }

},

        viewJob(id) {

            this.$router.push(

                `/student/jobs/${id}`

            );

        },

        logout() {

    localStorage.removeItem("token");

    this.$router.push("/");

},

        viewApplication(id) {

            this.$router.push(

                `/student/applications/${id}`

            );

        },

        async searchJobs() {

    try {

        const token = localStorage.getItem("token");

        const response = await axios.get(
            "http://127.0.0.1:5000/api/student/search-jobs",
            {
                params: {
                    q: this.search
                },
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        this.jobs = response.data;

    }

    catch (error) {

        console.error(error);

    }

},
 viewInterview(id) {

    this.$router.push(

        `/student/applications/${id}`

    );

},

    }

};
</script>