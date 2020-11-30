import FeeWaiverForm from '../../feewaiver_form.vue'
import FeeWaiverSubmit from '../feewaiver_submit.vue'
//import ExternalDashboard from '../dashboard.vue'
//import Proposal from '../proposal.vue'
//import CommercialOperatorLicence from '../commercial_operator_licence.vue'
export default
{
    path: '/external',
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
            component: FeeWaiverForm,
            name: 'external-feewaiver-form'
        },
        {
            path: 'submit',
            component: FeeWaiverSubmit,
            name:"submit_feewaiver"
        },
        /*
        {
            path: '/',
            component: ExternalDashboard,
            name: 'external-proposals-dash'
        },
        {
            path: 'organisations/manage/:org_id',
            component: Organisation
        },
        {
            path: 'compliance/:compliance_id',
            component: Compliance
        },
        {
            path: 'compliance/submit',
            component: ComplianceSubmit,
            name:"submit_compliance"
        },
        {
            path: 'approval/:approval_id',
            component: Approval,
        },
        {
            path: 'payment',
            component: PaymentDash,
            props: { level: 'external' }
        },
        {
            path: 'payment_order',
            component: PaymentOrder,
            name:"payment_order"
        },
        {
            path: 'proposal',
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
                    component: ProposalApply,
                    name:"apply_proposal"
                },
                {
                    path: 'submit',
                    component: ProposalSubmit,
                    name:"submit_proposal"
                },
                {
                    path: ':proposal_id',
                    component: Proposal,
                    name:"draft_proposal"
                },
                //{
                //    path: ':proposal_id',
                //    component: CommercialOperatorLicence,
                //    name:"draft_commercial_operator_licence"
                //},
            ]
        }
        */
    ]
}
