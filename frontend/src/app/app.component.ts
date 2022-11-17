import {Component, OnInit} from '@angular/core'
import {Internship, InternshipsService} from "../_generated/api";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  internships: Internship[] = []

  lorem: string = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent a tortor a nibh maximus varius. Nullam lacus urna, porta eget consequat eget, vestibulum eget nulla. Aliquam ac tellus quis ex laoreet bibendum. Sed sed pellentesque tellus. Pellentesque viverra, purus ut tincidunt pellentesque, leo metus pulvinar sem, vel condimentum leo metus ut magna. Etiam malesuada posuere sapien, non feugiat ante rutrum in. Ut malesuada nisl lacus, ac tincidunt ante rutrum ut. Curabitur quis nulla eu arcu ullamcorper aliquam. Nulla accumsan orci non ante fermentum, et auctor augue ultrices. Sed et sapien nunc. Curabitur rutrum libero eget bibendum interdum. In hac habitasse platea dictumst. Donec efficitur quam enim, nec pretium dolor hendrerit et. Vivamus in vulputate nulla. Nam et tempus ante, at interdum nisi.\n' +
    '\n' +
    'Suspendisse dolor metus, blandit et augue nec, mollis pharetra diam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur finibus eget nulla at finibus. Curabitur nec consectetur lorem. Duis dapibus dui at mi condimentum efficitur. Ut dignissim leo eu turpis finibus aliquet. Vestibulum semper diam faucibus, imperdiet quam molestie, porta dolor. Pellentesque tempor fringilla elit, vitae mollis diam tempor nec. Quisque imperdiet magna ut urna interdum finibus.\n' +
    '\n' +
    'Praesent a molestie dui. Cras porttitor justo a arcu aliquet, et scelerisque turpis mattis. Proin ullamcorper est est, eget laoreet lectus sagittis ut. Nunc id lorem id odio bibendum tristique in in enim. Vivamus nec ornare nibh. Quisque eget tortor feugiat, convallis libero eu, tristique lacus. Suspendisse porta eros ac tincidunt luctus. Etiam sed odio eget risus faucibus fringilla. Mauris lacus nisl, malesuada ut lorem vel, rhoncus accumsan neque. Maecenas tortor massa, dapibus vitae libero eget, aliquam vehicula arcu. Ut laoreet interdum suscipit.\n' +
    '\n' +
    'Nam non lectus vel massa tincidunt tempor nec id lorem. Ut in orci pellentesque, vulputate ante in, mattis mi. Praesent vel ipsum ac turpis gravida dapibus. Quisque vel convallis velit. Fusce quis eleifend ipsum. Nunc non enim mauris. Donec condimentum finibus congue. Vestibulum ullamcorper risus id dui lobortis, in hendrerit quam maximus. Etiam a est in turpis congue sagittis. Nulla a nibh urna. Proin imperdiet non nibh in molestie. Suspendisse non est in lectus bibendum malesuada. Quisque blandit vitae eros ut vehicula. Aenean vitae ex sit amet urna ornare luctus vel ut elit. Vivamus egestas semper dui, et lacinia arcu semper et. Vestibulum finibus quis odio in tempor.\n' +
    '\n' +
    'Nam porttitor nisi non mi euismod tincidunt. Nam luctus in leo ut fringilla. Mauris pulvinar consequat nisl sit amet aliquet. Fusce vulputate gravida dignissim. Etiam fringilla eu quam quis varius. Nunc quis tempus enim. Duis non nibh vitae magna tincidunt venenatis ac a justo. Mauris aliquam odio nec massa volutpat laoreet. Quisque dolor leo, volutpat ac dolor vitae, ullamcorper rutrum metus. Nam nec eleifend neque, sit amet congue orci. Nam facilisis pulvinar nisl sit amet consequat. In eu velit at risus aliquet mollis. Vivamus non vehicula neque.\n' +
    '\n\n\n' +
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent a tortor a nibh maximus varius. Nullam lacus urna, porta eget consequat eget, vestibulum eget nulla. Aliquam ac tellus quis ex laoreet bibendum. Sed sed pellentesque tellus. Pellentesque viverra, purus ut tincidunt pellentesque, leo metus pulvinar sem, vel condimentum leo metus ut magna. Etiam malesuada posuere sapien, non feugiat ante rutrum in. Ut malesuada nisl lacus, ac tincidunt ante rutrum ut. Curabitur quis nulla eu arcu ullamcorper aliquam. Nulla accumsan orci non ante fermentum, et auctor augue ultrices. Sed et sapien nunc. Curabitur rutrum libero eget bibendum interdum. In hac habitasse platea dictumst. Donec efficitur quam enim, nec pretium dolor hendrerit et. Vivamus in vulputate nulla. Nam et tempus ante, at interdum nisi.\n' +
    '\n' +
    'Suspendisse dolor metus, blandit et augue nec, mollis pharetra diam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur finibus eget nulla at finibus. Curabitur nec consectetur lorem. Duis dapibus dui at mi condimentum efficitur. Ut dignissim leo eu turpis finibus aliquet. Vestibulum semper diam faucibus, imperdiet quam molestie, porta dolor. Pellentesque tempor fringilla elit, vitae mollis diam tempor nec. Quisque imperdiet magna ut urna interdum finibus.\n' +
    '\n' +
    'Praesent a molestie dui. Cras porttitor justo a arcu aliquet, et scelerisque turpis mattis. Proin ullamcorper est est, eget laoreet lectus sagittis ut. Nunc id lorem id odio bibendum tristique in in enim. Vivamus nec ornare nibh. Quisque eget tortor feugiat, convallis libero eu, tristique lacus. Suspendisse porta eros ac tincidunt luctus. Etiam sed odio eget risus faucibus fringilla. Mauris lacus nisl, malesuada ut lorem vel, rhoncus accumsan neque. Maecenas tortor massa, dapibus vitae libero eget, aliquam vehicula arcu. Ut laoreet interdum suscipit.\n' +
    '\n' +
    'Nam non lectus vel massa tincidunt tempor nec id lorem. Ut in orci pellentesque, vulputate ante in, mattis mi. Praesent vel ipsum ac turpis gravida dapibus. Quisque vel convallis velit. Fusce quis eleifend ipsum. Nunc non enim mauris. Donec condimentum finibus congue. Vestibulum ullamcorper risus id dui lobortis, in hendrerit quam maximus. Etiam a est in turpis congue sagittis. Nulla a nibh urna. Proin imperdiet non nibh in molestie. Suspendisse non est in lectus bibendum malesuada. Quisque blandit vitae eros ut vehicula. Aenean vitae ex sit amet urna ornare luctus vel ut elit. Vivamus egestas semper dui, et lacinia arcu semper et. Vestibulum finibus quis odio in tempor.\n' +
    '\n' +
    'Nam porttitor nisi non mi euismod tincidunt. Nam luctus in leo ut fringilla. Mauris pulvinar consequat nisl sit amet aliquet. Fusce vulputate gravida dignissim. Etiam fringilla eu quam quis varius. Nunc quis tempus enim. Duis non nibh vitae magna tincidunt venenatis ac a justo. Mauris aliquam odio nec massa volutpat laoreet. Quisque dolor leo, volutpat ac dolor vitae, ullamcorper rutrum metus. Nam nec eleifend neque, sit amet congue orci. Nam facilisis pulvinar nisl sit amet consequat. In eu velit at risus aliquet mollis. Vivamus non vehicula neque.'

  async ngOnInit() {
    this.internships = await InternshipsService.getAllInternships()
  }
}
