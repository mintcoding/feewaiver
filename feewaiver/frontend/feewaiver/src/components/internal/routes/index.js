import InternalDashboard from '../dashboard.vue'
import FeeWaiverAssessment from '../assessment.vue'
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
            component: InternalDashboard,
            name:"fee-waiver-dash"
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
                    component: FeeWaiverAssessment,
                    name:"fee-waiver-assessment"
                },
            ]
        },
    ]
}
