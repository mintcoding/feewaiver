import FeeWaiverForm from '../../feewaiver_form.vue'
import FeeWaiverSubmit from '../feewaiver_submit.vue'
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
    ]
}
