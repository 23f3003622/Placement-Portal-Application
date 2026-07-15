<template>
<div class="container mt-4">

    <!-- Header -->
    <div class="card shadow mb-4">
        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center py-3">
            <div>
                <h2 class="mb-1">Next Step</h2>
                <p class="mb-0">Application Details</p>
            </div>

            <button
                class="btn btn-light"
                @click="$router.back()"
            >
                Back
            </button>
        </div>
    </div>

    <!-- Student Information -->
    <div class="card shadow mb-4">

        <div class="card-header bg-primary text-white">
            Student Information
        </div>

        <div class="card-body">

            <table class="table table-bordered align-middle">

                <tbody>

                    <tr>
                        <th width="25%">Name</th>
                        <td>{{ application.student.name }}</td>
                    </tr>

                    <tr>
                        <th>Email</th>
                        <td>{{ application.student.email }}</td>
                    </tr>

                    <tr>
                        <th>Branch</th>
                        <td>{{ application.student.branch }}</td>
                    </tr>

                    <tr>
                        <th>Year</th>
                        <td>{{ application.student.year }}</td>
                    </tr>

                    <tr>
                        <th>CGPA</th>
                        <td>{{ application.student.cgpa }}</td>
                    </tr>

                    <tr>
                        <th>Skills</th>
                        <td>{{ application.student.skills }}</td>
                    </tr>

                    <tr>
                        <th>Resume</th>

                        <td>
                            <a
                                :href="application.student.resume"
                                target="_blank"
                                class="btn btn-outline-primary btn-sm"
                            >
                                View Resume
                            </a>
                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

    </div>

    <!-- Status -->
    <div class="card shadow mb-4">

        <div class="card-header bg-primary text-white">
            Application Status
        </div>

        <div class="card-body">

            <div class="mb-3">

                <label class="form-label fw-bold">
                    Status
                </label>

                <select
                    class="form-select"
                    v-model="application.status"
                >
                    <option>Applied</option>
                    <option>Shortlisted</option>
                    <option>Selected</option>
                    <option>Rejected</option>
                </select>

            </div>

            <div>

                <label class="form-label fw-bold">
                    Remarks
                </label>

                <textarea
                    rows="4"
                    class="form-control"
                    v-model="application.remarks"
                ></textarea>

            </div>

        </div>

    </div>

    <!-- Interview -->
    <div
        v-if="application.status === 'Shortlisted'"
        class="card shadow mb-4"
    >

        <div class="card-header bg-primary text-white">
            Schedule Interview
        </div>

        <div class="card-body">

            <div class="mb-3">

                <label class="form-label">
                    Interview Type
                </label>

                <select
                    class="form-select"
                    v-model="interview.type"
                >
                    <option value="Online">Online</option>
                    <option value="In Person">In Person</option>
                </select>

            </div>

            <div class="mb-3">

                <label class="form-label">
                    Date
                </label>

                <input
                    type="date"
                    class="form-control"
                    v-model="interview.date"
                >

            </div>

            <div class="mb-3">

                <label class="form-label">
                    Time
                </label>

                <input
                    type="time"
                    class="form-control"
                    v-model="interview.time"
                >

            </div>

            <div class="mb-3">

                <label class="form-label">
                    Meeting Link / Venue
                </label>

                <input
                    type="text"
                    class="form-control"
                    placeholder="Google Meet link or Office Address"
                    v-model="interview.location"
                >

            </div>

            <button
                class="btn btn-primary"
                @click="scheduleInterview"
            >
                Schedule Interview
            </button>

        </div>

    </div>

    <!-- Buttons -->
    <div class="d-flex gap-2 mb-5">

        <button
            class="btn btn-success"
            @click="saveStatus"
        >
            Save Changes
        </button>

        <button
            v-if="application.status === 'Selected'"
            class="btn btn-warning"
            @click="sendOfferLetter"
        >
            Send Offer Letter
        </button>

    </div>

</div>
</template>

<script>
import axios from "axios";

export default {

    data() {

        return {

            application: {

                id: null,

                status: "Applied",

                remarks: "",

                student: {}

            },

            interview: {

                type: "Online",

                date: "",

                time: "",

                location: ""

            }

        };

    },

    async mounted() {
    console.log("Route Param:", this.$route.params.id);
    await this.loadApplication();
},

    methods: {

        async loadApplication() {

            try {

                const token = localStorage.getItem("token");

                const response = await axios.get(

                    `http://127.0.0.1:5000/api/company/applications/${this.$route.params.id}`,

                    {

                        headers: {

                            Authorization: `Bearer ${token}`

                        }

                    }

                );
                        console.log("Application Response:", response.data);

                this.application = response.data;
                if(response.data.interview){

    this.interview.type =
        response.data.interview.type || "Online";

    this.interview.date =
        response.data.interview.date || "";

    this.interview.time =
        response.data.interview.time || "";

    this.interview.location =
        response.data.interview.link ||
        response.data.interview.location ||
        "";

}
                console.log("Application ID:", this.application.id);

            }

            catch (error) {

                console.error(error);

                if (error.response) {

                    alert(error.response.data.message);

                }

            }

        },

        async saveStatus() {

            try {

                const token = localStorage.getItem("token");

                await axios.put(

                    `http://127.0.0.1:5000/api/company/applications/${this.application.id}/status`,

                    {

                        status: this.application.status,

                        remarks: this.application.remarks

                    },

                    {

                        headers: {

                            Authorization: `Bearer ${token}`

                        }

                    }

                );

                alert("Application updated successfully.");

            }

            catch (error) {

                console.error(error);

                if (error.response) {

                    alert(error.response.data.message);

                }

            }

        },

        async scheduleInterview() {

    console.log("Application:", this.application);

    if (!this.application.id) {
        alert("Application ID is missing.");
        return;
    }

    const token = localStorage.getItem("token");

    await axios.post(
        `http://127.0.0.1:5000/api/company/applications/${this.application.id}/schedule-interview`,
        this.interview,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    alert("Interview Scheduled Successfully.");
},

async sendOfferLetter() {

    const token = localStorage.getItem("token");

    try {

        await axios.post(

            `http://127.0.0.1:5000/api/company/applications/${this.application.id}/send-offer`,

            {},

            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }

        );

        alert("Offer letter sent successfully.");

    }

    catch(error){

        console.error(error);

        alert("Failed to send offer letter.");

    }

}

        
            

        

    }

};
</script>