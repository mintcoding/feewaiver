import InternalDashboard from '../dashboard.vue'
//import Search from '../search.vue'
import FeeWaiverForm from '../../feewaiver_form.vue'
export default
{
    path: '/internal',
    component:
    {
        render(c)
        {
            return c('router-view')
        }
    },
    children: [
        {
            path: '/',
            component: InternalDashboard
        },
        {
            path: 'fee_waiver',
            component: {
                render(c)
                {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: ':fee_waiver_id',
                    component: FeeWaiverForm,
                    name:"fee-waiver-details"
                },
            ]
        },

        /*
        {
            path: 'approvals',
            component: ApprovalDash,
            name:"internal-approvals-dash"
        },
        {
            path: 'approval/:approval_id',
            component: Approval,

        },
        {
            path: 'compliances',
            component: ComplianceDash,
            name:"internal-compliances-dash"
        },
        {
            path: 'compliance/:compliance_id',
            component: Compliance,

        },
        {
            path: 'search',
            component: Search,
            name:"internal-search"
        },
        // {
        //     path: 'payment',
        //     component: PaymentDash,
        //     props: { level: 'internal' }
        //     //component: PaymentOrder,
        // },
        // {
        //     path: 'payment',
        //     component: ParkBookingDash,
        //     props: { level: 'internal' }
        // },
        {
            path: 'payment',
            component: ParkEntryFeesDashboard,
        },
        {
            path: 'payment_order',
            component: PaymentOrder,
            name:"payment_order"
        },
        {
            path:'reports',
            name:'reports',
            component:Reports
        },

        {
            path: 'organisations',
            component: {
                render(c)
                {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: 'access',
                    component: OrgAccessTable,
                    name:"org-access-dash"
                },
                {
                    path: 'access/:access_id',
                    component: OrgAccess,
                    name:"org-access"
                },
                {
                    path: ':org_id',
                    component: Organisation,
                    name:"internal-org-detail"
                },

            ]
        },
        {
            path: 'users',
            component: {
                render(c)
                {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: ':user_id',
                    component: User,
                    name:"internal-user-detail"
                },
            ]
        },
        {
            path: 'proposal',
            component: {
                render(c)
                {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: ':proposal_id',
                    component: {
                        render(c)
                        {
                            return c('router-view')
                        }
                    },
                    children: [
                        {
                            path: '/',
                            component: Proposal,
                            name:"internal-proposal"
                        },
                        {
                            path: 'referral/:referral_id',
                            component: Referral,
                            name:"internal-referral"
                        },
                        {
                            path: 'district_proposal/:district_proposal_id',
                            component: DistrictProposal,
                            name:"internal-district-proposal"
                        },
                    ]
                },
            ]
        },
        {
            path: 'proposal_compare',
            component: {
                render(c)
                {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: ':proposal_id',
                    component: {
                        render(c)
                        {
                            return c('router-view')
                        }
                    },
                    children: [
                        {
                            path: '/',
                            component: ProposalCompare,
                            name:"proposal-compare"
                        }
                    ]
                },
            ]
        },
        */
    ]
}
