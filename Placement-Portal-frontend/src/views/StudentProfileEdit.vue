<template>
    <div class="container mt-4">

        <div class="card shadow">

            <div class="card-header bg-primary text-white">
                <h3>Edit Profile</h3>
            </div>

            <div class="card-body">

                <form @submit.prevent="updateProfile">

                    <div class="mb-3">
    <label class="form-label">Full Name</label>

    <input
        type="text"
        class="form-control"
        v-model="student.full_name"
        readonly
    >

    <small class="text-muted">
        Full name cannot be changed.
    </small>
</div>

                    <div class="row">

                        <div class="col-md-6 mb-3">
                            <label class="form-label">Branch</label>

                            <select
                                class="form-select"
                                v-model="student.branch"
                            >
                                <option>CSE</option>
                                <option>IT</option>
                                <option>ECE</option>
                                <option>EE</option>
                                <option>ME</option>
                                <option>CE</option>
                            </select>

                        </div>

                        <div class="col-md-6 mb-3">

                            <label class="form-label">Year</label>

                            <select
                                class="form-select"
                                v-model="student.year"
                            >
                                <option>1</option>
                                <option>2</option>
                                <option>3</option>
                                <option>4</option>
                            </select>

                        </div>

                    </div>

                    <div class="row">

                        <div class="col-md-6 mb-3">

                            <label class="form-label">CGPA</label>

                            <input
                                type="number"
                                step="0.01"
                                class="form-control"
                                v-model="student.cgpa"
                            >

                        </div>

                        <div class="col-md-6 mb-3">

                            <label class="form-label">Phone</label>

                            <input
                                type="text"
                                class="form-control"
                                v-model="student.phone"
                            >

                        </div>

                    </div>

                    <div class="mb-3">

                        <label class="form-label">
                            Skills
                        </label>

                        <textarea
                            rows="4"
                            class="form-control"
                            placeholder="Python, SQL, Machine Learning..."
                            v-model="student.skills"
                        ></textarea>

                    </div>

                    <div class="mb-3">

                        <label class="form-label">
                            Resume
                        </label>

                        <input
                            type="text"
                            class="form-control"
                            placeholder="Resume URL or filename"
                            v-model="student.resume"
                        >

                    </div>

                    <div class="mb-4">

                        <label class="form-label">
                            Experience
                        </label>

                        <textarea
                            rows="4"
                            class="form-control"
                            placeholder="Internships, Projects..."
                            v-model="student.experience"
                        ></textarea>

                    </div>

                    <button
                        class="btn btn-success"
                    >
                        Save Changes
                    </button>

                    <button
                        type="button"
                        class="btn btn-secondary ms-2"
                        @click="$router.push('/student')"
                    >
                        Cancel
                    </button>

                </form>

            </div>

        </div>

    </div>
</template>

<script>
import axios from "axios";

export default {

    data() {

        return {

            student: {

                full_name: "",
                branch: "",
                year: "",
                cgpa: "",
                phone: "",
                skills: "",
                resume: "",
                experience: ""

            }

        };

    },

    async mounted() {

        this.loadProfile();

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

            catch(error){

                console.log(error);

            }

        },

        async updateProfile() {

            try {

                const token = localStorage.getItem("token");

                const response = await axios.put(

                    "http://127.0.0.1:5000/api/student/profile",

                    this.student,

                    {

                        headers: {

                            Authorization: `Bearer ${token}`

                        }

                    }

                );

                alert(response.data.message);

                this.$router.push("/student");

            }

            catch(error){

                console.log(error);

                alert("Unable to update profile.");

            }

        }

    }

};
</script>