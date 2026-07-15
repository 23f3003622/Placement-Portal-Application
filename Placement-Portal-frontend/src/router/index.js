import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import AdminStudentDetails from "../views/AdminStudentDetails.vue";
import AdminCompanyDetails from "../views/AdminCompanyDetails.vue";
import CompanyDashboard from "../views/CompanyDashboard.vue";
import CreateDrive from "../views/CreateDrive.vue";
import UpcomingDrives from "../views/UpcomingDrives.vue";
import CompanyApplications from '../views/CompanyApplications.vue'
import CompanyApplicationDetails from '../views/CompanyApplicationDetails.vue'
import CompanyInterviews from "../views/CompanyInterviews.vue";
import StudentDashboard from "../views/StudentDashboard.vue";
import StudentJobDetails from "../views/StudentJobDetails.vue";
import StudentApplicationDetails from "../views/StudentApplicationDetails.vue";
import StudentHistory from "../views/StudentHistory.vue";
import StudentProfileEdit from "../views/StudentProfileEdit.vue";

const routes = [
  {
    path: "/",
    component: LoginView
  },
  {
    path: "/register",
    component: RegisterView
  },
  {
    path: "/student/history",
    component: StudentHistory
},
{
    path: "/company/interviews",
    component: CompanyInterviews
},
{
    path: "/student/profile/edit",
    component: StudentProfileEdit
},
{
    path: "/upcoming-drives",
    component: UpcomingDrives
},
  {
    path: "/admin",
    component: AdminDashboard
  },
  {
    path: "/admin/student/:id",
    component: AdminStudentDetails
},
{
    path: "/admin/company/:id",
    component: AdminCompanyDetails
},

  {
    path: "/student",
    component: StudentDashboard
  },
  {
    path: "/company/create-drive",
    component: CreateDrive
  },
  {
    path: "/company/dashboard",
    component: CompanyDashboard
},
  {
    path: "/company",
    component: CompanyDashboard
},
{
    path: "/company/jobs/:id/applications",
    component: CompanyApplications
},
{
    path: "/company/applications/:id",
    component: CompanyApplicationDetails
},
{
    path: "/student/jobs/:id",
    component: StudentJobDetails
},
{
    path: "/student/applications/:id",
    component: StudentApplicationDetails
},
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;