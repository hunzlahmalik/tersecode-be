## URLS

| URL | Params | Description | Done |
|---|---|---|---|
**Account**
| `/account/` | `{}` | Redirects to `/account/<username>` if loggedin else `/account/login` | `Yes` |
| `/account/login` | `{}` | Shows the login page | `Yes` |
| `/account/logout` | `{}` | Logs the user out | `Yes` |
| `/account/signup` | `{}` | Shows the register page | `Yes` |
| `/account/<username>` | `{}` | Shows the account page | `Yes` |
| `/account/<username>/update` | `{}` | Updates the user's account | `Yes` |
| `/account/<username>/delete` | `{}` | Deletes the user's account | `No` |
**Problem**
| `/problems/` | `{}` | List all the problems | `Yes` |
| `/problems/<id>` | `{}` | Show the single problem | `Yes` |
| `/problems/<id>/solution` | `{}` | Show the solution of the problem | `No` |
| `/problems/<id>/submit` | `{}` | Allows the user to submit solution | `Yes` |
**Submissions**
| `/submissions/` | `{}` | List all the submissions of current user | `Yes` |
| `/submissions/<id>` | `{}` | Show the single submission | `Yes` |

