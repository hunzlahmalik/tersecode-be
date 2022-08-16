## API

| API | Params | Description | Available |
|---|---|---|---|
**Account**
| `GET /account/` | `{}` | Shows the current user if logged in else 403 | `No` |
| `/account/login` | `{}` | Shows the login page | `No` |
| `/account/logout` | `{}` | Logs the user out | `No` |
| `/account/signup` | `{}` | Shows the register page | `No` |
| `/account/<username>` | `{}` | Shows the account page | `No` |
| `/account/<username>/update` | `{}` | Updates the user's account | `No` |
| `/account/<username>/delete` | `{}` | Deletes the user's account | `No` |
**Problem**
| `/problems/` | `{}` | List all the problems | `No` |
| `/problems/<id>` | `{}` | Show the single problem | `No` |
| `/problems/<id>/solution` | `{}` | Show the solution of the problem | `No` |
| `/problems/<id>/submit` | `{}` | Allows the user to submit solution | `No` |
**Submissions**
| `/submissions/` | `{}` | List all the submissions of current user | `No` |
| `/submissions/<id>` | `{}` | Show the single submission | `No` |

